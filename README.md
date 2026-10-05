# Secure Backend API

A secure RESTful backend application built with FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, role-based access control, file upload validation, logging, automated testing, and Docker.

## Features

* User registration and login
* Secure password hashing using Argon2
* JWT-based authentication
* Role-based access control (RBAC)
* Protected API endpoints
* PostgreSQL database integration
* SQLAlchemy ORM
* Alembic database migrations
* Secure file uploads with:

  * File extension validation
  * Maximum file size validation
  * Unique filenames
* Application logging
* Automated API testing with pytest
* Dockerized FastAPI backend
* Docker Compose with PostgreSQL
* Persistent database, upload, and log storage
* Environment-based configuration and secrets

## Technology Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT
* Argon2
* pytest
* Docker
* Docker Compose

## Project Structure

```text
secure-backend/
|-- app/
|   |-- core/
|   |   |-- config.py
|   |   |-- logging_config.py
|   |   `-- security.py
|   |-- database/
|   |   |-- base.py
|   |   `-- connection.py
|   |-- dependencies/
|   |   |-- auth.py
|   |   `-- roles.py
|   |-- models/
|   |   `-- user.py
|   |-- routes/
|   |   |-- auth.py
|   |   |-- files.py
|   |   `-- users.py
|   |-- schemas/
|   |   |-- auth.py
|   |   `-- user.py
|   |-- services/
|   |   `-- file_service.py
|   `-- __init__.py
|-- tests/
|   |-- test_auth.py
|   |-- test_files.py
|   |-- test_users.py
|   `-- __init__.py
|-- migrations/
|-- uploads/
|-- logs/
|-- .env.example
|-- .gitignore
|-- .dockerignore
|-- Dockerfile
|-- docker-compose.yml
|-- alembic.ini
|-- create_admin.py
|-- requirements.txt
`-- README.md
```

## Authentication

The application provides user registration and login APIs.

Passwords are never stored as plain text. Passwords are hashed using Argon2 before being stored in PostgreSQL.

After successful login, the server generates a JWT access token.

The token contains the authenticated user's identity and role and is required to access protected endpoints.

## Role-Based Access Control

The application supports two roles:

* `user`
* `admin`

Regular authenticated users can access their own profile.

Admin-only endpoints require the authenticated user to have the `admin` role.

Unauthorized users receive appropriate HTTP error responses.

## API Endpoints

### Authentication

| Method | Endpoint         | Description                 |
| ------ | ---------------- | --------------------------- |
| POST   | `/auth/register` | Register a new user         |
| POST   | `/auth/login`    | Login and receive JWT token |

### Users

| Method | Endpoint       | Authentication     |
| ------ | -------------- | ------------------ |
| GET    | `/users/me`    | Authenticated user |
| GET    | `/users/admin` | Admin only         |

### Files

| Method | Endpoint        | Authentication     |
| ------ | --------------- | ------------------ |
| POST   | `/files/upload` | Authenticated user |

### Health / Root

| Method | Endpoint | Description                      |
| ------ | -------- | -------------------------------- |
| GET    | `/`      | Check whether the API is running |

## File Upload Security

Uploaded files are validated before being stored.

The application:

* Allows only selected file extensions
* Limits files to 5 MB
* Generates unique filenames using UUIDs
* Requires authentication for file uploads
* Stores uploaded files separately from application source code

Allowed extensions:

```text
.jpg
.jpeg
.png
.pdf
```

## Logging

Application events are logged to:

```text
logs/app.log
```

The application records events such as:

* Successful registration
* Login attempts
* File uploads
* Authentication failures

Sensitive information such as passwords and JWT tokens is not logged.

## Database

PostgreSQL is used as the relational database.

SQLAlchemy provides ORM functionality, while Alembic manages database schema migrations.

Run migrations with:

```bash
alembic upgrade head
```

## Testing

The project uses pytest and FastAPI's TestClient.

Tests cover:

* API availability
* User registration
* User login
* JWT-protected profile access
* RBAC authorization
* File upload validation
* Authentication requirements

Run all tests:

```bash
pytest
```

Current test result:

```text
7 passed
```

## Dockerization

The backend is containerized using Docker.

Docker Compose runs two services:

```text
backend
    |
    `-- FastAPI application

db
    |
    `-- PostgreSQL
```

The project uses:

* `Dockerfile` to build the FastAPI application image
* `docker-compose.yml` to manage the backend and PostgreSQL services
* PostgreSQL named volume for database persistence
* Bind mounts for uploads and application logs
* PostgreSQL health check
* Environment variables for application configuration

### Start the Application

Create a `.env` file based on `.env.example` and configure the required values.

Then run:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Run database migrations inside the backend container:

```bash
docker compose exec backend alembic upgrade head
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### Stop the Application

```bash
docker compose down
```

## Environment Variables

Sensitive configuration is stored in `.env`.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/secure_backend
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file is excluded from Git using `.gitignore`.

## Security Practices

* Passwords are hashed before database storage
* JWT authentication protects private endpoints
* Role-based authorization protects admin endpoints
* Secret keys are loaded from environment variables
* `.env` is excluded from version control
* File extensions are validated
* File size is restricted
* Uploaded filenames are randomized
* Sensitive authentication data is not written to logs

## Project Purpose

This project demonstrates the implementation of a secure backend application using modern backend development practices, including authentication, authorization, database management, API security, file handling, logging, automated testing, and containerization.
