from fastapi.testclient import TestClient

from app.main import app


def test_allowed_host():
    with TestClient(app) as client:
        response = client.get(
            "/health"
        )

    assert response.status_code == 200


def test_untrusted_host_is_rejected():
    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={
                "Host": "evil.example.com",
            },
        )

    assert response.status_code == 400
