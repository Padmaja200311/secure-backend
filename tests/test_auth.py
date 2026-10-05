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