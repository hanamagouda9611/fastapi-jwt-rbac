
# FastAPI JWT RBAC

A simple FastAPI application that implements JWT authentication and **Role-Based Access Control (RBAC)**. This project allows you to register users, log in with JWT tokens, and restrict access to certain endpoints based on user roles (e.g., `admin`, `user`).

---

##  Project Structure

    fastapi-jwt-rbac/
    ├─ main.py             # Application entry point
    ├─ models.py           # SQLModel data models and schemas
    ├─ database.py         # Async database setup and session handling
    ├─ auth.py             # Authentication logic, JWT handling, password hashing
    ├─ project_routes.py   # Project-related routes (CRUD, RBAC protected)
    ├─ requirements.txt    # Python dependencies
    ├─ secretkey.py        # Generate the secretkey
    └─ README.md           # Project documentation

---

## Features

### JWT Authentication :
-- Secure token-based authentication using python-jose to issue and verify JWTs.

### Password Hashing :
-- Passwords are securely hashed using passlib[bcrypt] before being stored in the database.

### Role-Based Access Control (RBAC) :
-- Two user roles are supported:

  admin: Full access to all project operations (create, update, delete).

  user: Can only view project listings.

### Protected Endpoints with Dependency Injection :
-- Uses FastAPI's Depends(...) to restrict access based on authentication and user role.

### Asynchronous ORM with SQLModel + SQLite :
-- Utilizes SQLModel with async support and SQLite (easy to switch to PostgreSQL or others).

### CORS (Cross-Origin Resource Sharing) :
-- CORS enabled via FastAPI middleware for frontend/backend integration.

### Interactive API Documentation :
-- Built-in Swagger UI and ReDoc, with full Bearer Token authentication support in the docs.

---

## Endpoints Summary

| Method | Path                         | Role Required | Description                   |
|--------|------------------------------|---------------|-------------------------------|
| POST   | `/register`                  | None          | Register new user or admin    |
| POST   | `/login`                     | None          | Login and get JWT token       |
| GET    | `/projects/`                 | user/admin    | List all projects             |
| POST   | `/projects/`                 | admin         | Create a new project          |
| PUT    | `/projects/{project_id}`     | admin         | Update a project              |
| DELETE | `/projects/{project_id}`     | admin         | Delete a project              |

---

## Roles

- `admin`: Full access (create, update, delete projects)
- `user`: Can only view project list
- Username + Role must be **unique** when registering

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hanamagouda9611/fastapi-jwt-rbac.git
cd fastapi-jwt-api
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app 

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000 
```

### 4. API Docs

Swagger UI: http://localhost:5000/docs

ReDoc: http://localhost:5000/redoc

### 5. Authentication Flow

Register using /register
Login using /login to get the JWT token
Use the token as a Bearer Token in Authorization header to access protected endpoints

```bash
Authorization: Bearer <your_token_here>
```
