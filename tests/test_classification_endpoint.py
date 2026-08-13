import pytest
from fastapi.testclient import TestClient

from app.api.dependencies.rate_limit import (
    enforce_rate_limit,
)
from app.api.routes.classification import (
    get_classification_service,
)
from app.domain.classification import (
    ClassificationPrediction,
)
from app.main import app
from app.schemas.classification import (
    ClassificationResponse,
)


class FakeClassificationService:
    def classify(self, request):
        return ClassificationResponse(
            language={
                "code": request.language,
                "confidence": None,
            },
            classification=[
                ClassificationPrediction(
                    label="technology",
                    confidence=0.9,
                ),
                ClassificationPrediction(
                    label="sports",
                    confidence=0.1,
                ),
            ],
        )


@pytest.fixture
def client():
    app.dependency_overrides[
        get_classification_service
    ] = lambda: FakeClassificationService()

    app.dependency_overrides[
        enforce_rate_limit
    ] = lambda: object()

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(
        get_classification_service,
        None,
    )

    app.dependency_overrides.pop(
        enforce_rate_limit,
        None,
    )


def test_classification_endpoint(client):
    response = client.post(
        "/v1/classify",
        json={
            "text": (
                "Apple released a new processor."
            ),
            "candidate_labels": [
                "technology",
                "sports",
            ],
            "language": "en",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["language"]["code"]
        == "en"
    )

    assert (
        data["classification"][0]["label"]
        == "technology"
    )

    assert (
        data["classification"][0][
            "confidence"
        ]
        == 0.9
    )
