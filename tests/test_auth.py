from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Secure Backend API is running"
    }


def test_register_user():
    unique_id = uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"pytestuser_{unique_id}",
            "email": f"pytest_{unique_id}@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == f"pytest_{unique_id}@example.com"
    assert data["role"] == "user"
    assert "hashed_password" not in data


def test_login_user():
    unique_id = uuid4().hex[:8]

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"loginuser_{unique_id}",
            "email": f"login_{unique_id}@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": f"login_{unique_id}@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password():
    unique_id = uuid4().hex[:8]

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"wrongpass_{unique_id}",
            "email": f"wrongpass_{unique_id}@example.com",
            "password": "Test@12345"
        }
    )

    assert register_response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": f"wrongpass_{unique_id}@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_protected_endpoint_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401

def test_protected_endpoint_with_malformed_token():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer malformed.jwt.token"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"

def test_register_duplicate_email():
    unique_id = uuid4().hex[:8]

    user_data = {
        "username": f"duplicate_{unique_id}",
        "email": f"duplicate_{unique_id}@example.com",
        "password": "Test@12345"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            **user_data,
            "username": f"duplicate_second_{unique_id}"
        }
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "Username or email already exists"
    )