# Scholarship Finder Application

## Overview
The Scholarship Finder Application is designed to help students discover scholarships that match their qualifications and needs. Users can filter scholarships based on various criteria such as type, country, and requirements, as well as sort them by application deadlines. The application provides a RESTful API for easy integration with front-end applications or other services.

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
        "title": "National Merit Scholarship",
        "description": "Awarded to high school students based on academic achievement.",
        "type": "merit-based",
        "country": "USA",
        "requirements": ["GPA above 3.5", "SAT score above 1400"],
        "deadline": "2023-12-01"
      },
      ...
    ]
    ```

### 2. Create a New Scholarship
