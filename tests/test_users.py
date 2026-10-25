
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user_and_get_token():
    unique_id = uuid4().hex[:8]
    username = f"pytestuser_{unique_id}"
    email = f"pytestuser_{unique_id}@example.com"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    return email, login_response.json()["access_token"]


def test_get_my_profile():
    email, token = create_user_and_get_token()

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["role"] == "user"


def test_admin_access_denied_for_user():
    _, token = create_user_and_get_token()

    response = client.get(
        "/users/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
