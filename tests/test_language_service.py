from app.domain.language import LanguagePrediction
from app.services.language import LanguageService


class FakeLanguageDetector:
    def detect(self, text: str) -> LanguagePrediction:
        return LanguagePrediction(
            code="es",
            confidence=0.98,
        )


def test_language_service_uses_detector():
    service = LanguageService(
        detector=FakeLanguageDetector()
    )

    result = service.detect("Me encantó este producto.")

    assert result.code == "es"
    assert result.confidence == 0.98


def test_confident_language_uses_detected_code():
    detector = FakeLanguageDetector()

    service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    prediction = LanguagePrediction(
        code="es",
        confidence=0.98,
    )

    assert service.routing_language(prediction) == "es"


def test_low_confidence_language_uses_fallback():
    detector = FakeLanguageDetector()

    service = LanguageService(
        detector=detector,
        min_confidence=0.70,
    )

    prediction = LanguagePrediction(
        code="es",
        confidence=0.31,
    )

    assert service.routing_language(prediction) == "*"