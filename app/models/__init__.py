from typing import Protocol

from app.models.sentiment import SentimentModel
from app.schemas.sentiment import (
    SentimentRequest,
    SentimentResponse,
)


class SentimentAnalyzer(Protocol):
    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        ...


class SentimentService:
    def __init__(self, model: SentimentModel):
        self._model = model

    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        prediction = self._model.predict(request.text)

        return SentimentResponse(
            language=request.language,
            sentiment=prediction,
        )