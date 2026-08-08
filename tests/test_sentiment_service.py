from app.domain.language import LanguagePrediction
from app.domain.sentiment import (
    SentimentLabel,
    SentimentPrediction,
)
from app.models.registry import ModelRegistry
from app.schemas.sentiment import SentimentRequest
from app.services.language import LanguageService
from app.services.sentiment import SentimentService


class FakeSentimentModel:
    def predict(self, text: str) -> SentimentPrediction:
        return SentimentPrediction(
            label=SentimentLabel.POSITIVE,
            confidence=0.91,
        )


class FakeLanguageDetector:
    def detect(self, text: str) -> LanguagePrediction:
        return LanguagePrediction(
            code="es",
            confidence=0.98,
        )


def test_sentiment_service_uses_registry_model():
    registry = ModelRegistry()

    registry.register(
        "sentiment",
        "es",
        FakeSentimentModel,
    )

    language_service = LanguageService(
        detector=FakeLanguageDetector()
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="Me encantó.",
        language="es",
    )

    result = service.analyze(request)

    assert result.language.code == "es"
    assert result.sentiment.label == SentimentLabel.POSITIVE
    assert result.sentiment.confidence == 0.91


def test_sentiment_service_detects_language_when_not_provided():
    registry = ModelRegistry()

    registry.register(
        "sentiment",
        "es",
        FakeSentimentModel,
    )

    language_service = LanguageService(
        detector=FakeLanguageDetector()
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="Me encantó.",
    )

    result = service.analyze(request)

    assert result.language.code == "es"
    assert result.language.confidence == 0.98