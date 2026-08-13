from typing import Any, Protocol

from transformers import pipeline

from app.domain.ner import EntityLabel, EntityPrediction
from app.models.errors import ModelOutputError
from app.models.lazy import ThreadSafeLazyLoader


MODEL_NAME = "Davlan/xlm-roberta-base-ner-hrl"

LABEL_MAP = {
    "PER": EntityLabel.PERSON,
    "ORG": EntityLabel.ORGANIZATION,
    "LOC": EntityLabel.LOCATION,
}


class TokenClassifier(Protocol):
    def __call__(self, text: str, **kwargs: Any) -> list[dict[str, Any]]:
        ...


class DavlanMultilingualNERModel:
    def __init__(self, classifier: TokenClassifier | None = None) -> None:
        self._classifier_loader = (
            ThreadSafeLazyLoader(
                factory=self._create_classifier,
                value=classifier,
            )
        )

    def _create_classifier(self):
        return pipeline(
            "token-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            aggregation_strategy="simple",
        )

    def _get_classifier(self):
        return self._classifier_loader.get()

    def predict(self, text: str) -> list[EntityPrediction]:
        results = self._get_classifier()(text)

        entities = []

        for result in results:
            raw_label = str(result["entity_group"]).upper()

            if raw_label not in LABEL_MAP:
                raise ModelOutputError(
                    f"Unexpected NER label: {raw_label!r}"
                )

            start = int(result["start"])
            end = int(result["end"])

            entities.append(
                EntityPrediction(
                    text=text[start:end],
                    label=LABEL_MAP[raw_label],
                    start=start,
                    end=end,
                    confidence=round(float(result["score"]), 4),
                )
            )

        return entities
