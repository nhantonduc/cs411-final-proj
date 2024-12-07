#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create a user
create_user() {
  echo "Creating a new user..."
  curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}' | grep -q '"status": "user added"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to log out a user
logout_user() {
  echo "Logging out user..."
  response=$(curl -s -X POST "$BASE_URL/logout" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  if echo "$response" | grep -q '"message": "User testuser logged out successfully."'; then
    echo "User logged out successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Logout Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log out user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

##############################################
#
# Scholarship
#
##############################################

# Function to get all scholarships
get_all_scholarships() {
    echo "Getting all scholarships..."
    response=$(curl -s -X GET "$BASE_URL/scholarships")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Retrieved all scholarships successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to retrieve scholarships."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

# Function to get scholarships by type
get_scholarships_by_type() {
    local scholarship_type="merit"  # Example type
    echo "Getting scholarships of type: $scholarship_type..."
    response=$(curl -s -X GET "$BASE_URL/scholarships/type/$scholarship_type")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Retrieved scholarships by type successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to retrieve scholarships by type."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

# Function to get scholarships sorted by deadline
get_scholarships_by_deadline() {
    echo "Getting scholarships sorted by deadline..."
    response=$(curl -s -X GET "$BASE_URL/scholarships/sort/deadline")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Retrieved sorted scholarships successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to retrieve sorted scholarships."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

##############################################
#
# Favorites
#
##############################################

# Function to get user's favorites
get_user_favorites() {
    local user_id=1  # Example user ID
    echo "Getting favorites for user $user_id..."
    response=$(curl -s -X GET "$BASE_URL/favorites/$user_id")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Retrieved favorites successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to retrieve favorites."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

# Function to add a scholarship to favorites
add_to_favorites() {
    echo "Adding scholarship to favorites..."
    response=$(curl -s -X POST "$BASE_URL/favorites/add" \
        -H "Content-Type: application/json" \
        -d '{"user_id": 1, "scholarship_id": 1111}')
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Added scholarship to favorites successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to add scholarship to favorites."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

# Function to remove a scholarship from favorites
remove_from_favorites() {
    echo "Removing scholarship from favorites..."
    response=$(curl -s -X POST "$BASE_URL/favorites/remove" \
        -H "Content-Type: application/json" \
        -d '{"user_id": 1, "scholarship_id": 1111}')
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Removed scholarship from favorites successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Response JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to remove scholarship from favorites."
        if [ "$ECHO_JSON" = true ]; then
            echo "Error Response JSON:"
            echo "$response" | jq .
        fi
        exit 1
    fi
}

# Main test sequence
main() {
    echo "Starting smoke tests..."
    
    # Health check
    check_health
    
    # User management tests
    create_user
    login_user
    
    # Scholarship tests
    get_all_scholarships
    get_scholarships_by_type
    get_scholarships_by_deadline
    
    # Favorites tests
    get_user_favorites
    add_to_favorites
    get_user_favorites  # Verify addition
    remove_from_favorites
    get_user_favorites  # Verify removal
    
    # Cleanup
    logout_user
    delete_user
    
    echo "All smoke tests completed successfully!"
}

# Run the tests
main "$@"