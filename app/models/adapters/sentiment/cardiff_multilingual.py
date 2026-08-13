from typing import Any, Protocol

from transformers import pipeline

from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.models.errors import ModelOutputError
from app.models.lazy import ThreadSafeLazyLoader


MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

LABEL_MAP = {
    "negative": SentimentLabel.NEGATIVE,
    "neutral": SentimentLabel.NEUTRAL,
    "positive": SentimentLabel.POSITIVE,
}


class TextClassifier(Protocol):
    def __call__(self, text: str, **kwargs: Any) -> list[dict[str, Any]]:
        ...


class CardiffMultilingualSentimentModel:
    def __init__(self, classifier: TextClassifier | None = None) -> None:
        self._classifier_loader = (
            ThreadSafeLazyLoader(
                factory=self._create_classifier,
                value=classifier,
            )
        )

    def _create_classifier(self):
        return pipeline(
            "text-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
        )

    def _get_classifier(self):
        return self._classifier_loader.get()

    def predict(self, text: str) -> SentimentPrediction:
        result = self._get_classifier()(
            text,
            truncation=True,
        )[0]

        raw_label = str(result["label"]).lower()

        if raw_label not in LABEL_MAP:
            raise ModelOutputError(
                f"Unexpected sentiment label: {raw_label!r}"
            )

        return SentimentPrediction(
            label=LABEL_MAP[raw_label],
            confidence=round(float(result["score"]), 4),
        )