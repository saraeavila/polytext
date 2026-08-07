from typing import Protocol

from app.models.registry import ModelRegistry
from app.schemas.sentiment import SentimentRequest, SentimentResponse


class SentimentAnalyzer(Protocol):
    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        ...


class SentimentService:
    def __init__(self, registry: ModelRegistry):
        self._registry = registry

    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        model = self._registry.get(
            task="sentiment",
            language=request.language,
        )

        prediction = model.predict(request.text)

        return SentimentResponse(
            language=request.language,
            sentiment=prediction,
        )