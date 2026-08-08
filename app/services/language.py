from app.domain.language import LanguagePrediction
from app.models.language import LanguageDetector


class LanguageService:
    def __init__(self, detector: LanguageDetector):
        self._detector = detector

    def detect(self, text: str) -> LanguagePrediction:
        return self._detector.detect(text)