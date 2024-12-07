from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
# from flask_cors import CORS

from config import ProductionConfig
from scholarship_finder.db import db
from scholarship_finder.models.user_model import Users
from scholarship_finder.models.favorites_model import FavoritesModel
from scholarship_finder.models.scholarship_model import ScholarshipModel
from datetime import datetime
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
            Users.create_user(username, password)

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
            Users.delete_user(username)

            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    ##########################################################
    #
    # Scholarship Routes
    #
    ##########################################################

    @app.route('/api/scholarships', methods=['GET'])
    def get_all_scholarships():
        """Get all available scholarships."""
        try:
            scholarships = ScholarshipModel.get_all_scholarships()
            return jsonify({
                "status": "success",
                "scholarships": scholarships
            }), 200
        except Exception as e:
            app.logger.error(f"Error retrieving scholarships: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve scholarships"
            }), 500

    @app.route('/api/scholarships/type/<scholarship_type>', methods=['GET'])
    def get_scholarships_by_type(scholarship_type):
        """Get scholarships filtered by type."""
        try:
            scholarships = ScholarshipModel.get_scholarships_by_type(scholarship_type)
            return jsonify({
                "status": "success",
                "scholarships": scholarships,
                "type": scholarship_type
            }), 200
        except Exception as e:
            app.logger.error(f"Error retrieving scholarships by type: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve scholarships"
            }), 500

    @app.route('/api/scholarships/sort/deadline', methods=['GET'])
    def get_scholarships_by_deadline():
        """Get scholarships sorted by deadline."""
        try:
            scholarships = ScholarshipModel.get_scholarships_sorted_by_deadline()
            return jsonify({
                "status": "success",
                "scholarships": scholarships
            }), 200
        except Exception as e:
            app.logger.error(f"Error retrieving sorted scholarships: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve sorted scholarships"
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
            scholarship_id = data.get('scholarship_id')

            if not user_id or not scholarship_id:
                return jsonify({
                    "status": "error",
                    "message": "Missing user_id or scholarship_id"
                }), 400

            favorites_model = FavoritesModel(user_id)
            favorites_model.add_to_favorites(scholarship_id)

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
            scholarship_id = data.get('scholarship_id')

            if not user_id or not scholarship_id:
                return jsonify({
                    "status": "error",
                    "message": "Missing user_id or scholarship_id"
                }), 400

            favorites_model = FavoritesModel(user_id)
            favorites_model.remove_from_favorites(scholarship_id)

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

    if __name__ == '__main__':
        app.run(debug=True)

