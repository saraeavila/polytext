from typing import Protocol

from app.models.registry import ModelRegistry
from app.schemas.language import LanguageInfo
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.language import LanguageService


class SentimentAnalyzer(Protocol):
    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        ...


class SentimentService:
    def __init__(
        self,
        registry: ModelRegistry,
        language_service: LanguageService,
    ):
        self._registry = registry
        self._language_service = language_service

    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        language = self._language_service.resolve(
            text=request.text,
            requested_language=request.language,
        )

        model = self._registry.get(
            task="sentiment",
            language=language.routing_language,
        )

        prediction = model.predict(request.text)

        return SentimentResponse(
            language=LanguageInfo(
                code=language.code,
                confidence=language.confidence,
            ),
            sentiment=prediction,
        )
