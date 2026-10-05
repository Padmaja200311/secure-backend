from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_my_profile():

    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytestuser2@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "pytestuser2@example.com"
    assert data["role"] == "user"


def test_admin_access_denied_for_user():

    login_response = client.post(
        "/auth/login",
        json={
            "email": "pytestuser2@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"