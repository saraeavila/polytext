from fastapi.testclient import TestClient

from app.api.routes.sentiment import get_sentiment_service
from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.main import app
from app.schemas.sentiment import SentimentResponse


class FakeSentimentService:
    def analyze(self, request):
        return SentimentResponse(
            language=request.language,
            sentiment=SentimentPrediction(
                label=SentimentLabel.POSITIVE,
                confidence=0.95,
            ),
        )


def override_sentiment_service():
    return FakeSentimentService()


app.dependency_overrides[get_sentiment_service] = override_sentiment_service

client = TestClient(app)


def test_sentiment_endpoint():
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Me encantó este producto.",
            "language": "es",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "language": "es",
        "sentiment": {
            "label": "positive",
            "confidence": 0.95,
        },
    }


def test_sentiment_endpoint_normalizes_language():
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Great product.",
            "language": "EN",
        },
    )

    assert response.status_code == 200
    assert response.json()["language"] == "en"


def test_sentiment_endpoint_rejects_blank_text():
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "   ",
            "language": "en",
        },
    )

    assert response.status_code == 422


def test_sentiment_endpoint_rejects_invalid_language():
    response = client.post(
        "/v1/sentiment",
        json={
            "text": "Great product.",
            "language": "potato!!",
        },
    )

    assert response.status_code == 422