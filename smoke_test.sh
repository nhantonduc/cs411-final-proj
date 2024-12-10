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
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
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
  response=$(curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"status": "user added"'; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to delete a user
delete_user() {
  echo "Deleting user..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  if echo "$response" | grep -q '"status": "user deleted"'; then
    echo "User deleted successfully."
  else
    echo "Failed to delete user."
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
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Failed to retrieve scholarships."
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
  local user_id=1
  echo "Getting favorites for user $user_id..."
  response=$(curl -s -X GET "$BASE_URL/favorites/$user_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Retrieved favorites successfully."
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Failed to retrieve favorites."
    exit 1
  fi
}

# Function to add a scholarship to favorites
add_to_favorites() {
  echo "Adding scholarship to favorites..."
  response=$(curl -s -X POST "$BASE_URL/favorites/add" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 1,
      "scholarship": {
        "university": "Test University",
        "scholarship_name": "Test Scholarship",
        "type": "merit",
        "degree_level": "Undergraduate",
        "country": "USA",
        "deadline": "2024-12-31",
        "min_gpa": 3.5,
        "major": [{"name": "Computer Science"}]
      }
    }')
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Added scholarship to favorites successfully."
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Failed to add scholarship to favorites."
    exit 1
  fi
}

# Function to remove a scholarship from favorites
remove_from_favorites() {
  echo "Removing scholarship from favorites..."
  response=$(curl -s -X POST "$BASE_URL/favorites/remove" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": 1,
      "scholarship": {
        "university": "Test University",
        "scholarship_name": "Test Scholarship",
        "type": "merit",
        "degree_level": "Undergraduate",
        "country": "USA",
        "deadline": "2024-12-31",
        "min_gpa": 3.5,
        "major": [{"name": "Computer Science"}]
      }
    }')
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Removed scholarship from favorites successfully."
    [ "$ECHO_JSON" = true ] && echo "$response" | jq .
  else
    echo "Failed to remove scholarship from favorites."
    exit 1
  fi
}

# Function to clear all favorites for a user
clear_favorites() {
  echo "Clearing all favorites for user..."
  response=$(curl -s -X POST "$BASE_URL/favorites/clear" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1}')
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Cleared all favorites successfully."
  else
    echo "Failed to clear favorites."
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

  # Scholarship tests
  get_all_scholarships

  # Favorites tests
  add_to_favorites
  get_user_favorites  # Verify addition
  remove_from_favorites
  get_user_favorites  # Verify removal
  clear_favorites

  # Cleanup
  delete_user

  echo "All smoke tests completed successfully!"
}

# Run the tests
main "$@"
