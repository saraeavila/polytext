from fastapi.testclient import TestClient

from app.main import app


def test_sentiment_requires_api_key():
    with TestClient(app) as client:
        response = client.post(
            "/v1/sentiment",
            json={
                "text": "Great product.",
                "language": "en",
            },
        )

    assert response.status_code == 401


def test_entities_requires_api_key():
    with TestClient(app) as client:
        response = client.post(
            "/v1/entities",
            json={
                "text": "Sara visited Madrid.",
                "language": "en",
            },
        )

    assert response.status_code == 401
