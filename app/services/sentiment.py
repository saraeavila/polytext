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
        if request.language is not None:
            routing_language = request.language

            language = LanguageInfo(
                code=request.language,
                confidence=None,
            )

        else:
            prediction = self._language_service.detect(request.text)

            routing_language = self._language_service.routing_language(
                prediction
            )

            language = LanguageInfo(
                code=prediction.code,
                confidence=prediction.confidence,
            )

        model = self._registry.get(
            task="sentiment",
            language=routing_language,
        )

        prediction = model.predict(request.text)

        return SentimentResponse(
            language=language,
            sentiment=prediction,
        )
