from typing import Protocol

from app.domain.language import LanguagePrediction


class LanguageDetector(Protocol):
    def detect(self, text: str) -> LanguagePrediction:
        ...

class PlaceholderLanguageDetector:
    def detect(self, text: str) -> LanguagePrediction:
        raise NotImplementedError(
            "Language detection has not been configured."
        )