from app.domain.language import LanguagePrediction
from app.domain.ner import EntityLabel, EntityPrediction
from app.models.registry import ModelRegistry
from app.schemas.ner import NERRequest
from app.services.language import LanguageService
from app.services.ner import NERService


class FakeNERModel:
    def predict(self, text: str) -> list[EntityPrediction]:
        return [
            EntityPrediction(
                text="Madrid",
                label=EntityLabel.LOCATION,
                start=13,
                end=19,
                confidence=0.96,
            )
        ]


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
        task="ner",
        language="*",
        factory=FakeNERModel,
    )

    return registry


def test_ner_uses_detected_language():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="es",
        confidence=0.98,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = NERService(
        registry=registry,
        language_service=language_service,
    )

    request = NERRequest(
        text="Sara visitó Madrid."
    )

    result = service.analyze(request)

    assert detector.called is True
    assert result.language.code == "es"
    assert result.language.confidence == 0.98

    assert len(result.entities) == 1
    assert result.entities[0].text == "Madrid"


def test_explicit_ner_language_skips_detection():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="en",
        confidence=0.99,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = NERService(
        registry=registry,
        language_service=language_service,
    )

    request = NERRequest(
        text="Sara visitó Madrid.",
        language="es",
    )

    result = service.analyze(request)

    assert detector.called is False
    assert result.language.code == "es"
    assert result.language.confidence is None


def test_low_confidence_ner_detection_uses_fallback():
    registry = create_test_registry()

    detector = FakeLanguageDetector(
        code="es",
        confidence=0.25,
    )

    language_service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    service = NERService(
        registry=registry,
        language_service=language_service,
    )

    request = NERRequest(
        text="Sara visitó Madrid."
    )

    result = service.analyze(request)

    assert result.language.code == "es"
    assert result.language.confidence == 0.25

    assert len(result.entities) == 1
