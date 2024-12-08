# Scholarship Finder Application

## Overview
The Scholarship Finder Application is designed to help students discover scholarships that match their qualifications and needs. Users can filter scholarships based on various criteria, manage their favorites, and access detailed information about each scholarship. The application provides a RESTful API for easy integration with front-end applications or other services.

## API Routes

### 1. Get All Scholarships
- **Route Name and Path**: Get Scholarships - `/api/scholarships`
- **Request Type**: GET
- **Purpose**: Retrieve a list of all available scholarships.
- **Request Format**: 
  - No parameters required.
- **Response Format**: 
  - JSON object containing an array of scholarships.
  - Example JSON keys:
    - `id`: integer
    - `title`: string
    - `description`: string
    - `type`: string
    - `country`: string
    - `requirements`: array of strings
    - `deadline`: string (ISO 8601 date format)
- **Example**:
  - **Request**: 
    ```bash
    curl -X GET http://localhost:5000/api/scholarships
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

### 2. Create a New Scholarship
- **Route Name and Path**: Create Scholarship - `/api/scholarships`
- **Request Type**: POST
- **Purpose**: Add a new scholarship to the database.
- **Request Format**: 
  - POST body:
    ```json
    {
      "title": "New Scholarship",
      "description": "Description of the new scholarship.",
      "type": "need-based",
      "country": "USA",
      "requirements": ["Financial need", "Essay submission"],
      "deadline": "2024-01-15"
    }
    ```
- **Response Format**: 
  - JSON object containing the created scholarship.
- **Example**:
  - **Request**: 
    ```bash
    curl -X POST http://localhost:5000/api/scholarships -H "Content-Type: application/json" -d '{"title": "New Scholarship", "description": "Description of the new scholarship.", "type": "need-based", "country": "USA", "requirements": ["Financial need", "Essay submission"], "deadline": "2024-01-15"}'
    ```
  - **Response**:
    ```json
    {
      "id": 2,
      "title": "New Scholarship",
      "description": "Description of the new scholarship.",
      "type": "need-based",
      "country": "USA",
      "requirements": ["Financial need", "Essay submission"],
      "deadline": "2024-01-15"
    }
    ```

### 3. Update a Scholarship
- **Route Name and Path**: Update Scholarship - `/api/scholarships/<id>`
- **Request Type**: PUT
- **Purpose**: Update an existing scholarship by its ID.
- **Request Format**: 
  - PUT body:
    ```json
    {
      "title": "Updated Scholarship Title",
      "description": "Updated description.",
      "type": "merit-based",
      "country": "USA",
      "requirements": ["Updated requirement"],
      "deadline": "2024-02-01"
    }
    ```
- **Response Format**: 
  - JSON object containing the updated scholarship.
- **Example**:
  - **Request**: 
    ```bash
    curl -X PUT http://localhost:5000/api/scholarships/1 -H "Content-Type: application/json" -d '{"title": "Updated Scholarship Title", "description": "Updated description.", "type": "merit-based", "country": "USA", "requirements": ["Updated requirement"], "deadline": "2024-02-01"}'
    ```
  - **Response**:
    ```json
    {
      "id": 1,
      "title": "Updated Scholarship Title",
      "description": "Updated description.",
      "type": "merit-based",
      "country": "USA",
      "requirements": ["Updated requirement"],
      "deadline": "2024-02-01"
    }
    ```

### 4. Delete a Scholarship
- **Route Name and Path**: Delete Scholarship - `/api/scholarships/<id>`
- **Request Type**: DELETE
- **Purpose**: Remove a scholarship from the database by its ID.
- **Request Format**: 
  - No body required.
- **Response Format**: 
  - JSON object confirming deletion.
- **Example**:
  - **Request**: 
    ```bash
    curl -X DELETE http://localhost:5000/api/scholarships/1
    ```
  - **Response**:
    ```json
    {
      "message": "Scholarship deleted successfully."
    }
    ```

### 5. Get User's Favorite Scholarships
- **Route Name and Path**: Get Favorites - `/api/favorites`
- **Request Type**: GET
- **Purpose**: Retrieve a list of the user's favorite scholarships.
- **Request Format**: 
  - No parameters required.
- **Response Format**: 
  - JSON object containing an array of favorite scholarships.
- **Example**:
  - **Request**: 
    ```bash
    curl -X GET http://localhost:5000/api/favorites
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

### 6. Add a Scholarship to Favorites
- **Route Name and Path**: Add to Favorites - `/api/favorites`
- **Request Type**: POST
- **Purpose**: Add a scholarship to the user's favorites.
- **Request Format**: 
  - POST body:
    ```json
    {
      "scholarship_id": 1
    }
    ```
- **Response Format**: 
  - JSON object confirming the addition.
- **Example**:
  - **Request**: 
    ```bash
    curl -X POST http://localhost:5000/api/favorites -H "Content-Type: application/json" -d '{"scholarship_id": 1}'
    ```
  - **Response**:
    ```json
    {
      "message": "Scholarship added to favorites successfully."
    }
    ```

## Conclusion
This API provides a comprehensive way for users to find scholarships that fit their needs and manage their favorites. By utilizing the various filtering and management options, users can easily navigate through the available scholarships and make informed decisions about their applications.
