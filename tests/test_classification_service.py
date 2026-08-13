from app.domain.classification import (
    ClassificationPrediction,
)
from app.domain.language import (
    LanguageResolution,
)
from app.schemas.classification import (
    ClassificationRequest,
)
from app.services.classification import (
    ClassificationService,
)


class FakeClassificationModel:
    def predict(
        self,
        text,
        candidate_labels,
    ):
        return [
            ClassificationPrediction(
                label="technology",
                confidence=0.9,
            ),
            ClassificationPrediction(
                label="sports",
                confidence=0.1,
            ),
        ]


class FakeRegistry:
    def __init__(self):
        self.task = None
        self.language = None

    def get(
        self,
        task,
        language,
    ):
        self.task = task
        self.language = language

        return FakeClassificationModel()


class FakeLanguageService:
    def resolve(
        self,
        text,
        requested_language,
    ):
        return LanguageResolution(
            code="en",
            confidence=None,
            routing_language="en",
        )


def test_classification_service():
    registry = FakeRegistry()

    service = ClassificationService(
        registry=registry,
        language_service=(
            FakeLanguageService()
        ),
    )

    response = service.classify(
        ClassificationRequest(
            text="Apple released a processor.",
            candidate_labels=[
                "technology",
                "sports",
            ],
            language="en",
        )
    )

    assert registry.task == "classification"
    assert registry.language == "en"

    assert (
        response.language.code
        == "en"
    )

    assert (
        response.classification[0].label
        == "technology"
    )

    assert (
        response.classification[0].confidence
        == 0.9
    )
