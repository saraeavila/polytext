import pytest
from fastapi.testclient import TestClient

from app.api.dependencies.rate_limit import enforce_rate_limit
from app.api.routes.sentiment import get_sentiment_service
from app.main import app
from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.schemas.sentiment import SentimentResponse


class FakeSentimentService:
    def analyze(self, request):
        return SentimentResponse(
            language={
                "code": request.language,
                "confidence": None,
            },
            sentiment=SentimentPrediction(
                label=SentimentLabel.POSITIVE,
                confidence=0.95,
            ),
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_sentiment_service] = (
        lambda: FakeSentimentService()
    )

    app.dependency_overrides[enforce_rate_limit] = lambda: object()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(
        get_sentiment_service,
        None,
    )
    app.dependency_overrides.pop(
        enforce_rate_limit,
        None,
    )


def test_sentiment_endpoint(client):
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Me encantó este producto.",
            "language": "es",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "language": {
            "code": "es",
            "confidence": None,
        },
        "sentiment": {
            "label": "positive",
            "confidence": 0.95,
        },
    }


def test_sentiment_endpoint_normalizes_language(client):
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Great product.",
            "language": "EN",
        },
    )

    assert response.status_code == 200
    assert response.json()["language"]["code"] == "en"


def test_sentiment_endpoint_rejects_blank_text(client):
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "   ",
            "language": "en",
        },
    )

    assert response.status_code == 422


def test_sentiment_endpoint_rejects_invalid_language(client):
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Great product.",
            "language": "potato!!",
        },
    )

    assert response.status_code == 422
