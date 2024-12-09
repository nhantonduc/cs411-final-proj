# Scholarship Finder Application

## Overview

The Scholarship Finder Application is designed to help students discover scholarships that match their qualifications and needs. Users can filter scholarships based on various criteria, manage their favorites, and access detailed information about each scholarship.

## API Routes

### 1. Get Scholarships

- **Route**: `/api/scholarships`
- **Method**: GET
- **Query Parameters**:
  - `type` (str): Filter by scholarship type
  - `country` (str): Filter by country
  - `degree_level` (str): Filter by degree level
  - `min_gpa` (float): Filter by minimum GPA
  - `major` (str): Filter by major
  - `sort_by` (str): Sort results by field (e.g., 'deadline')
  - `sort_order` (str): Sort direction ('asc' or 'desc')
- **Response**:

### 2. Get Scholarships by Type

- **Route Name and Path**: Get Scholarships by Type - `/api/scholarships/type/<scholarship_type>`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships filtered by a specific type.
- **Request Format**:
  - URL parameter:
    - `scholarship_type`: string (the type of scholarship to filter by)
- **Response Format**:
  - JSON object containing an array of scholarships matching the specified type.
- **Example**:
  - **Request**:
    ```bash
    curl -X GET http://localhost:5000/api/scholarships/type/merit-based
    ```
  - **Response**:
    ```json
    [
      {
        "id": 1,
        "title": "National Merit Scholarship",
        "description": "Awarded to high school students based on academic achievement.",
        "type": "merit-based",
        "country": "USA",
        "requirements": ["GPA above 3.5", "SAT score above 1400"],
        "deadline": "2023-12-01"
      }
    ]
    ```

### 3. Sort Scholarships by Deadline

- **Route Name and Path**: Sort Scholarships by Deadline - `/api/scholarships/sort/deadline`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships sorted by their application deadlines in ascending order.
- **Request Format**:
  - No parameters required.
- **Response Format**:
  - JSON object containing an array of scholarships sorted by deadline.
- **Example**:
  - **Request**:
    ```bash
    curl -X GET http://localhost:5000/api/scholarships/sort/deadline
    ```
  - **Response**:
    ```json
    [
      {
        "id": 1,
        "title": "National Merit Scholarship",
        "description": "Awarded to high school students based on academic achievement.",
        "type": "merit-based",
        "country": "USA",
        "requirements": ["GPA above 3.5", "SAT score above 1400"],
        "deadline": "2023-12-01"
      }
    ]
    ```

### 4. Get User's Favorite Scholarships

- **Route Name and Path**: Get User's Favorites - `/api/favorites/<int:user_id>`
- **Request Type**: GET
- **Purpose**: Retrieve a list of the user's favorite scholarships.
- **Request Format**:
  - URL parameter:
    - `user_id`: integer (the ID of the user whose favorites are being retrieved)
- **Response Format**:
  - JSON object containing an array of favorite scholarships.
- **Example**:
  - **Request**:
    ```bash
    curl -X GET http://localhost:5000/api/favorites/1
    ```
  - **Response**:
    ```json
    [
      {
        "id": 1,
        "title": "National Merit Scholarship",
        "description": "Awarded to high school students based on academic achievement."
      }
    ]
    ```

### 5. Add a Scholarship to Favorites

- **Route Name and Path**: Add to Favorites - `/api/favorites/add`
- **Request Type**: POST
- **Purpose**: Add a scholarship to the user's favorites.
- **Request Format**:
  - POST body:
    ```json
    {
      "user_id": 1,
      "scholarship_id": 1
    }
    ```
- **Response Format**:
  - JSON object confirming the addition.
- **Example**:
  - **Request**:
    ```bash
    curl -X POST http://localhost:5000/api/favorites/add -H "Content-Type: application/json" -d '{"user_id": 1, "scholarship_id": 1}'
    ```
  - **Response**:
    ```json
    {
      "message": "Scholarship added to favorites successfully."
    }
    ```

### 6. Remove a Scholarship from Favorites

- **Route Name and Path**: Remove from Favorites - `/api/favorites/remove`
- **Request Type**: POST
- **Purpose**: Remove a scholarship from the user's favorites.
- **Request Format**:
  - POST body:
    ```json
    {
      "user_id": 1,
      "scholarship_id": 1
    }
    ```
- **Response Format**:
  - JSON object confirming the removal.
- **Example**:
  - **Request**:
    ```bash
    curl -X POST http://localhost:5000/api/favorites/remove -H "Content-Type: application/json" -d '{"user_id": 1, "scholarship_id": 1}'
    ```
  - **Response**:
    ```json
    {
      "message": "Scholarship removed from favorites successfully."
    }
    ```

## Conclusion

This API provides a comprehensive way for users to find scholarships that fit their needs and manage their favorites. By utilizing the various filtering and management options, users can easily navigate through the available scholarships and make informed decisions about their applications.
