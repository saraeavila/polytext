from app.domain.language import (
    LanguagePrediction,
    LanguageResolution,
)
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

    def resolve(
        self,
        text: str,
        requested_language: str | None,
    ) -> LanguageResolution:
        if requested_language is not None:
            return LanguageResolution(
                code=requested_language,
                confidence=None,
                routing_language=requested_language,
            )

        prediction = self.detect(text)

        return LanguageResolution(
            code=prediction.code,
            confidence=prediction.confidence,
            routing_language=self.routing_language(prediction),
        )
