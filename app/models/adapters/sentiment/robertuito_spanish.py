from typing import Any, Protocol

from transformers import pipeline

from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.models.errors import ModelOutputError


MODEL_NAME = "pysentimiento/robertuito-sentiment-analysis"

LABEL_MAP = {
    "POS": SentimentLabel.POSITIVE,
    "NEG": SentimentLabel.NEGATIVE,
    "NEU": SentimentLabel.NEUTRAL,
}


class TextClassifier(Protocol):
    def __call__(self, text: str, **kwargs: Any) -> list[dict[str, Any]]:
        ...


class RobertuitoSpanishSentimentModel:
    def __init__(self, classifier: TextClassifier | None = None) -> None:
        self._pipeline = classifier or pipeline(
            "text-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
        )

    def predict(self, text: str) -> SentimentPrediction:
        result = self._pipeline(
            text,
            truncation=True,
        )[0]

        raw_label = str(result["label"]).upper()

        if raw_label not in LABEL_MAP:
            raise ModelOutputError(
                f"Unexpected sentiment label: {raw_label!r}"
            )

        return SentimentPrediction(
            label=LABEL_MAP[raw_label],
            confidence=round(float(result["score"]), 4),
        )