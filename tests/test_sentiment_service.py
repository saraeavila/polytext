from app.domain.language import LanguagePrediction
from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.models.registry import ModelRegistry
from app.schemas.sentiment import SentimentRequest
from app.services.language import LanguageService
from app.services.sentiment import SentimentService


class FakeSpanishModel:
    def predict(self, text: str) -> SentimentPrediction:
        return SentimentPrediction(
            label=SentimentLabel.POSITIVE,
            confidence=0.91,
        )


class FakeMultilingualModel:
    def predict(self, text: str) -> SentimentPrediction:
        return SentimentPrediction(
            label=SentimentLabel.NEUTRAL,
            confidence=0.75,
        )


class FakeLanguageDetector:
    def __init__(self, code: str, confidence: float):
        self.code = code
        self.confidence = confidence
        self.called = False

    def detect(self, text: str) -> LanguagePrediction:
        self.called = True

        return LanguagePrediction(
            code=self.code,
            confidence=self.confidence,
        )


def create_test_registry() -> ModelRegistry:
    registry = ModelRegistry()

    registry.register(
        task="sentiment",
        language="es",
        factory=FakeSpanishModel,
    )

    registry.register(
        task="sentiment",
        language="*",
        factory=FakeMultilingualModel,
    )

    return registry


def test_detected_spanish_routes_to_specialist():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="es",
        confidence=0.98,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="Me encantó este producto."
    )

    result = service.analyze(request)

    assert detector.called is True

    assert result.language.code == "es"
    assert result.language.confidence == 0.98

    # Positive identifies the Spanish specialist.
    assert result.sentiment.label == SentimentLabel.POSITIVE
    assert result.sentiment.confidence == 0.91


def test_detected_english_routes_to_fallback():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="en",
        confidence=0.96,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="This product was great."
    )

    result = service.analyze(request)

    assert detector.called is True

    assert result.language.code == "en"
    assert result.language.confidence == 0.96

    # Neutral identifies the multilingual fallback.
    assert result.sentiment.label == SentimentLabel.NEUTRAL
    assert result.sentiment.confidence == 0.75


def test_low_confidence_detection_routes_to_fallback():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="es",
        confidence=0.31,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="Texto ambiguo."
    )

    result = service.analyze(request)

    assert detector.called is True

    # We still report what the detector predicted.
    assert result.language.code == "es"
    assert result.language.confidence == 0.31

    # But low confidence forces multilingual fallback routing.
    assert result.sentiment.label == SentimentLabel.NEUTRAL
    assert result.sentiment.confidence == 0.75


def test_explicit_language_skips_detection():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="en",
        confidence=0.99,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = SentimentService(
        registry=registry,
        language_service=language_service,
    )

    request = SentimentRequest(
        text="Me encantó este producto.",
        language="es",
    )

    result = service.analyze(request)

    assert detector.called is False

    assert result.language.code == "es"
    assert result.language.confidence is None

    assert result.sentiment.label == SentimentLabel.POSITIVE
    assert result.sentiment.confidence == 0.91