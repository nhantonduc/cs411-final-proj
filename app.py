from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
from scholarship_finder.utils.random_utils import fetch_scholarship_data
from pprint import pprint
# from flask_cors import CORS

from config import ProductionConfig
from scholarship_finder.db import db
from scholarship_finder.models.user_model import User
from scholarship_finder.models.favorites_model import FavoritesModel
from scholarship_finder.models.scholarship_model import Scholarship
from datetime import datetime
from scholarship_finder.models.mongo_session_model import login_user, logout_user
import logging

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    ##########################################################
    #
    # User management
    #
    ##########################################################

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the new user.
            - password (str): The password for the new user.

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the user to the database.
        """
        app.logger.info('Creating new user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

            # Call the User function to add the user to the database
            app.logger.info('Adding user: %s', username)
            User.create_user(username, password)

            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """
        Route to delete a user.

        Expected JSON Input:
            - username (str): The username of the user to be deleted.

        Returns:
            JSON response indicating the success of user deletion.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue deleting the user from the database.
        """
        app.logger.info('Deleting user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')

            if not username:
                return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

            # Call the User function to delete the user from the database
            app.logger.info('Deleting user: %s', username)
            User.delete_user(username)

            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
    
    @app.route('/api/login', methods=['POST'])
    def login():
        """
        Route to log in a user and load their favorites.
        
        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The user's password.

        Returns:
            JSON response indicating the success of the login.
        
        Raises:
            400 error if input validation fails.
            401 error if authentication fails (invalid username or password).
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            app.logger.error("Invalid request payload for login.")
            raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

        username = data['username']
        password = data['password']

        try:
            # Validate user credentials
            if not User.check_password(username, password):
                app.logger.warning("Login failed for username: %s", username)
                raise Unauthorized("Invalid username or password.")

            # Get user ID
            user_id = User.get_id_by_username(username)

            # Load user's favorites into the FavoritesModel
            favorites_model = FavoritesModel(user_id)
            login_user(user_id, favorites_model)  # Load favorites from MongoDB

            app.logger.info("User %s logged in successfully.", username)
            return jsonify({"message": f"User {username} logged in successfully.", "favorites": favorites_model.get_favorites()}), 200

        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    @app.route('/api/logout', methods=['POST'])
    def logout():
        """
        Route to log out a user and save their favorites to MongoDB.

        Expected JSON Input:
            - username (str): The username of the user.

        Returns:
            JSON response indicating the success of the logout.

        Raises:
            400 error if input validation fails or user is not found in MongoDB.
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data:
            app.logger.error("Invalid request payload for logout.")
            raise BadRequest("Invalid request payload. 'username' is required.")

        username = data['username']

        try:
            # Get user ID
            user_id = User.get_id_by_username(username)

            # Create a new FavoritesModel instance
            favorites_model = FavoritesModel(user_id)

            # Save user's favorites and clear the favorites model
            logout_user(user_id, favorites_model)  # Save favorites to MongoDB

            app.logger.info("User %s logged out successfully.", username)
            return jsonify({"message": f"User {username} logged out successfully."}), 200

        except ValueError as e:
            app.logger.warning("Logout failed for username %s: %s", username, str(e))
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error("Error during logout for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500

    ##########################################################
    #
    # Scholarship Routes
    #
    ##########################################################

    @app.route('/api/scholarships', methods=['GET'])
    def get_scholarships():
        """
        Get scholarships with optional filters.
        
        Query Parameters:
            type (str): Filter by scholarship type
            country (str): Filter by country
            degree_level (str): Filter by degree level
            min_gpa (float): Filter by minimum GPA
            major (str): Filter by major
            sort_by (str): Sort results by field (e.g., 'deadline')
            sort_order (str): Sort direction ('asc' or 'desc')
        
        Returns:
            JSON response with filtered scholarships
        """
        try:
            # Get all scholarships
            scholarships = fetch_scholarship_data()
            
            # Apply filters based on query parameters
            filters = request.args
            
            # Type filter
            if filters.get('type'):
                scholarships = [s for s in scholarships if s['type'] == filters['type']]
            
            # Country filter
            if filters.get('country'):
                scholarships = [s for s in scholarships if s['country'] == filters['country']]
            
            # Degree level filter
            if filters.get('degree_level'):
                scholarships = [s for s in scholarships if s['degree_level'] == filters['degree_level']]
            
            # Min GPA filter
            if filters.get('min_gpa'):
                try:
                    min_gpa = float(filters['min_gpa'])
                    scholarships = [s for s in scholarships if s['min_gpa'] and float(s['min_gpa']) >= min_gpa]
                except ValueError:
                    return jsonify({
                        "status": "error",
                        "message": "Invalid min_gpa value"
                    }), 400
            
            # Major filter
            if filters.get('major'):
                scholarships = [
                    s for s in scholarships 
                    if any(major['name'].lower() == filters['major'].lower() for major in s['major'])
                ]
            
            # Sorting
            sort_by = filters.get('sort_by', 'deadline')
            sort_order = filters.get('sort_order', 'asc')
            
            if sort_by in ['deadline', 'scholarship_name', 'university']:
                scholarships = sorted(
                    scholarships,
                    key=lambda x: (x[sort_by] is None, x[sort_by]),  # Handle None values
                    reverse=(sort_order.lower() == 'desc')
                )
            
            return jsonify({
                "status": "success",
                "filters_applied": dict(filters),
                "count": len(scholarships),
                "scholarships": scholarships
            }), 200
            
        except Exception as e:
            app.logger.error(f"Error retrieving scholarships: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve scholarships"
            }), 500

    ##########################################################
    #
    # Favorites Routes
    #
    ##########################################################

    @app.route('/api/favorites/<int:user_id>', methods=['GET'])
    def get_user_favorites(user_id):
        """Get all favorites for a specific user."""
        try:
            favorites_model = FavoritesModel(user_id)
            favorites = favorites_model.get_favorites()
            
            return jsonify({
                "status": "success",
                "favorites": favorites
            }), 200
        except Exception as e:
            app.logger.error(f"Error retrieving favorites for user {user_id}: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve favorites"
            }), 500

    @app.route('/api/favorites/add', methods=['POST'])
    def add_to_favorites():
        """Add a scholarship to user's favorites."""
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            scholarship_data = data.get('scholarship')

            if not user_id or not scholarship_data:
                return jsonify({
                    "status": "error",
                    "message": "Missing user_id or scholarship data"
                }), 400

            # Create Scholarship object from the received data
            scholarship = Scholarship(
                university=scholarship_data.get('university'),
                scholarship_name=scholarship_data.get('scholarship_name'),
                type=scholarship_data.get('type'),
                degree_level=scholarship_data.get('degree_level'),
                country=scholarship_data.get('country'),
                deadline=scholarship_data.get('deadline'),
                min_gpa=scholarship_data.get('min_gpa'),
                major=scholarship_data.get('major')
            )

            favorites_model = FavoritesModel(user_id)
            favorites_model.add_to_favorites(scholarship)

            return jsonify({
                "status": "success",
                "message": "Scholarship added to favorites"
            }), 200
        except Exception as e:
            app.logger.error(f"Error adding scholarship to favorites: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to add scholarship to favorites"
            }), 500

    @app.route('/api/favorites/remove', methods=['POST'])
    def remove_from_favorites():
        """Remove a scholarship from user's favorites."""
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            scholarship_data = data.get('scholarship')

            if not user_id or not scholarship_data:
                return jsonify({
                    "status": "error",
                    "message": "Missing user_id or scholarship data"
                }), 400

            # Create Scholarship object from the received data
            scholarship = Scholarship(
                university=scholarship_data.get('university'),
                scholarship_name=scholarship_data.get('scholarship_name'),
                type=scholarship_data.get('type'),
                degree_level=scholarship_data.get('degree_level'),
                country=scholarship_data.get('country'),
                deadline=scholarship_data.get('deadline'),
                min_gpa=scholarship_data.get('min_gpa'),
                major=scholarship_data.get('major')
            )

            favorites_model = FavoritesModel(user_id)
            favorites_model.remove_from_favorites(scholarship)

            return jsonify({
                "status": "success",
                "message": "Scholarship removed from favorites"
            }), 200
        except Exception as e:
            app.logger.error(f"Error removing scholarship from favorites: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to remove scholarship from favorites"
            }), 500

    @app.route('/api/favorites/clear', methods=['POST'])
    def clear_favorites():
        """Clear all favorites for a user."""
        try:
            data = request.get_json()
            user_id = data.get('user_id')

            if not user_id:
                return jsonify({
                    "status": "error",
                    "message": "Missing user_id"
                }), 400

            favorites_model = FavoritesModel(user_id)
            favorites_model.clear_favorites()

            return jsonify({
                "status": "success",
                "message": "All favorites cleared"
            }), 200
        except Exception as e:
            app.logger.error(f"Error clearing favorites: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to clear favorites"
            }), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    return app

if __name__ == '__main__':
        app = create_app()
        app.run(debug=True)