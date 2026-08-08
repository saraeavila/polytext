from app.domain.language import LanguagePrediction
from app.models.language import LanguageDetector


MIN_LANGUAGE_CONFIDENCE = 0.70


class LanguageService:
    def __init__(
        self,
        detector: LanguageDetector,
        min_confidence: float = MIN_LANGUAGE_CONFIDENCE,
    ):
        self._detector = detector
        self._min_confidence = min_confidence

    def detect(self, text: str) -> LanguagePrediction:
        return self._detector.detect(text)

    def routing_language(
        self,
        prediction: LanguagePrediction,
    ) -> str:
        if prediction.confidence < self._min_confidence:
            return "*"

        return prediction.code
