from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "pytestuser2@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_upload_valid_file():

    token = get_token()

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "file": (
                "test.pdf",
                BytesIO(b"%PDF-1.4 test file content"),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "File uploaded successfully"
    assert data["filename"].endswith(".pdf")


def test_upload_invalid_file_type():

    token = get_token()

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "file": (
                "test.txt",
                BytesIO(b"test file content"),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File type not allowed"


def test_upload_oversized_file():

    token = get_token()

    large_file = BytesIO(b"x" * (5 * 1024 * 1024 + 1))

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "file": (
                "large.pdf",
                large_file,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File size must be less than 5 MB"


def test_upload_without_authentication():

    response = client.post(
        "/files/upload",
        files={
            "file": (
                "test.pdf",
                BytesIO(b"%PDF-1.4 test file content"),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 401