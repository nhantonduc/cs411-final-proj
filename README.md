# Scholarship Finder API

## Overview

The Scholarship Finder API is designed to help users discover scholarships and manage their favorites. Users can filter scholarships based on criteria, add or remove favorites, and retrieve their favorite scholarships.

## API Routes

### 1. Get Scholarships

- **Route Name and Path**: Get Scholarships - `/api/scholarships`
- **Request Type**: GET
- **Purpose**: Retrieve scholarships with optional filters.
- **Query Parameters**:
  - `type` (str): Filter by scholarship type.
  - `country` (str): Filter by country.
  - `degree_level` (str): Filter by degree level.
  - `min_gpa` (float): Filter by minimum GPA.
  - `major` (str): Filter by major.
  - `sort_by` (str): Sort results by field (e.g., 'deadline').
  - `sort_order` (str): Sort direction (`asc` or `desc`).
- **Response Format**:
  - JSON object containing the list of scholarships matching the criteria.
- **Example**:
  - **Request**:
    ```bash
    curl -X GET "http://localhost:5000/api/scholarships?country=USA&type=merit-based"
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "filters_applied": {
        "country": "USA",
        "type": "merit-based"
      },
      "count": 2,
      "scholarships": [
        {
          "university": "Harvard University",
          "scholarship_name": "Harvard Merit Scholarship",
          "type": "Merit-based",
          "degree_level": "Undergraduate",
          "country": "USA",
          "deadline": "2024-01-15",
          "min_gpa": 3.5,
          "major": ["Computer Science"]
        }
      ]
    }
    ```

---

### 2. Get User Favorites

- **Route Name and Path**: Get User Favorites - `/api/favorites/<int:user_id>`
- **Request Type**: GET
- **Purpose**: Retrieve the list of scholarships saved as favorites by the user.
- **Path Parameters**:
  - `user_id`: The ID of the user.
- **Response Format**:
  - JSON object containing the user's favorite scholarships.
- **Example**:
  - **Request**:
    ```bash
    curl -X GET "http://localhost:5000/api/favorites/1"
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "favorites": [
        {
          "university": "MIT",
          "scholarship_name": "MIT STEM Scholarship"
        }
      ]
    }
    ```

---

### 3. Add to Favorites

- **Route Name and Path**: Add to Favorites - `/api/favorites/add`
- **Request Type**: POST
- **Purpose**: Add a scholarship to the user's favorites.
- **Request Format**:
  - JSON body:
    ```json
    {
      "user_id": 1,
      "scholarship": {
        "university": "MIT",
        "scholarship_name": "MIT STEM Scholarship",
        "type": "Merit-based",
        "degree_level": "Undergraduate",
        "country": "USA",
        "deadline": "2024-05-01",
        "min_gpa": 3.7,
        "major": ["Physics"]
      }
    }
    ```
- **Response Format**:
  - JSON object confirming the addition.
- **Example**:
  - **Request**:
    ```bash
    curl -X POST "http://localhost:5000/api/favorites/add" -H "Content-Type: application/json" -d '{"user_id":1,"scholarship":{"university":"MIT","scholarship_name":"MIT STEM Scholarship","type":"Merit-based","degree_level":"Undergraduate","country":"USA","deadline":"2024-05-01","min_gpa":3.7,"major":["Physics"]}}'
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "message": "Scholarship added to favorites."
    }
    ```

---

### 4. Remove from Favorites

- **Route Name and Path**: Remove from Favorites - `/api/favorites/remove`
- **Request Type**: POST
- **Purpose**: Remove a scholarship from the user's favorites.
- **Request Format**:
  - JSON body:
    ```json
    {
      "user_id": 1,
      "scholarship": {
        "university": "MIT",
        "scholarship_name": "MIT STEM Scholarship",
        "type": "Merit-based",
        "degree_level": "Undergraduate",
        "country": "USA",
        "deadline": "2024-05-01",
        "min_gpa": 3.7,
        "major": ["Physics"]
      }
    }
    ```
- **Response Format**:
  - JSON object confirming the removal.
- **Example**:
  - **Request**:
    ```bash
    curl -X POST "http://localhost:5000/api/favorites/remove" -H "Content-Type: application/json" -d '{"user_id":1,"scholarship":{"university":"MIT","scholarship_name":"MIT STEM Scholarship","type":"Merit-based","degree_level":"Undergraduate","country":"USA","deadline":"2024-05-01","min_gpa":3.7,"major":["Physics"]}}'
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "message": "Scholarship removed from favorites."
    }
    ```

---

### 5. Clear Favorites

- **Route Name and Path**: Clear Favorites - `/api/favorites/clear`
- **Request Type**: POST
- **Purpose**: Clear all favorite scholarships for a specific user.
- **Request Format**:
  - JSON body:
    ```json
    {
      "user_id": 1
    }
    ```
- **Response Format**:
  - JSON object confirming the clearing of favorites.
- **Example**:
  - **Request**:
    ```bash
    curl -X POST "http://localhost:5000/api/favorites/clear" -H "Content-Type: application/json" -d '{"user_id":1}'
    ```
  - **Response**:
    ```json
    {
      "status": "success",
      "message": "All favorites cleared."
    }
    ```

---

## Conclusion

The Scholarship Finder API simplifies the process of discovering scholarships and managing favorites, making it a valuable tool for students and users looking for financial aid opportunities.
