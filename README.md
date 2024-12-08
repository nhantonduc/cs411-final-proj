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

### 2. Filter Scholarships by Type
- **Route Name and Path**: Filter by Type - `/api/scholarships/type`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships filtered by a specific type.
- **Request Format**: 
  - GET parameters:
    - `type`: string (the type of scholarship to filter by)
- **Response Format**: 
  - JSON object containing an array of scholarships matching the specified type.
- **Example**:
  - **Request**: 
    ```bash
    curl -X GET "http://localhost:5000/api/scholarships/type?type=merit-based"
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
      }
    ]
    ```

### 3. Filter Scholarships by Country
- **Route Name and Path**: Filter by Country - `/api/scholarships/country`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships offered in a specific country.
- **Request Format**: 
  - GET parameters:
    - `country`: string (the country to filter by)
- **Response Format**: 
  - JSON object containing an array of scholarships offered in the specified country.
- **Example**:
  - **Request**: 
    ```bash
    curl -X GET "http://localhost:5000/api/scholarships/country?country=USA"
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
      }
    ]
    ```

### 4. Filter Scholarships by Requirements
- **Route Name and Path**: Filter by Requirements - `/api/scholarships/requirements`
- **Request Type**: POST
- **Purpose**: Retrieve scholarships that meet all specified requirements.
- **Request Format**: 
  - POST body:
    ```json
    {
      "requirements": ["GPA above 3.5", "SAT score above 1400"]
    }
    ```
- **Response Format**: 
  - JSON object containing an array of scholarships meeting the specified requirements.
- **Example**:
  - **Request**: 
    ```bash
    curl -X POST http://localhost:5000/api/scholarships/requirements -H "Content-Type: application/json" -d '{"requirements": ["GPA above 3.5", "SAT score above 1400"]}'
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
      }
    ]
    ```

### 5. Sort Scholarships by Deadline
- **Route Name and Path**: Sort by Deadline - `/api/scholarships/sort`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships sorted by their application deadlines in ascending order.
- **Request Format**: 
  - No parameters required.
- **Response Format**: 
  - JSON object containing an array of scholarships sorted by deadline.
- **Example**:
  - **Request**: 
    ```bash
    curl -X GET http://localhost:5000/api/scholarships/sort
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

## Conclusion
This API provides a comprehensive way for users to find scholarships that fit their needs. By utilizing the various filtering and sorting options, users can easily navigate through the available scholarships and make informed decisions about their applications.
