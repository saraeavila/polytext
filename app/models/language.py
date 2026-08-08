from typing import Protocol

from app.domain.language import LanguagePrediction


class LanguageDetector(Protocol):
    def detect(self, text: str) -> LanguagePrediction:
        ...

class PlaceholderLanguageDetector:
    def detect(self, text: str) -> LanguagePrediction:
        return LanguagePrediction(
            code="en",
            confidence=0.0,
        )