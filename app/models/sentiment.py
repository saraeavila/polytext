from typing import Protocol

from app.domain.sentiment import (
    SentimentLabel,
    SentimentPrediction,
)


class SentimentModel(Protocol):
    def predict(self, text: str) -> SentimentPrediction:
        ...


class PlaceholderSentimentModel:
    def predict(self, text: str) -> SentimentPrediction:
        return SentimentPrediction(
            label=SentimentLabel.NEUTRAL,
            confidence=0.0,
        )