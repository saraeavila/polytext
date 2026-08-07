from transformers import pipeline

from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.models.errors import ModelOutputError


MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

LABEL_MAP = {
    "negative": SentimentLabel.NEGATIVE,
    "neutral": SentimentLabel.NEUTRAL,
    "positive": SentimentLabel.POSITIVE,
}


class CardiffMultilingualSentimentModel:
    def __init__(self) -> None:
        self._pipeline = pipeline(
            "text-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
        )

    def predict(self, text: str) -> SentimentPrediction:
        result = self._pipeline(
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
            confidence=float(result["score"]),
        )
