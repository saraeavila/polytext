from collections.abc import Callable

from transformers import pipeline

from app.domain.classification import (
    ClassificationPrediction,
)
from app.models.errors import ModelOutputError


MODEL_NAME = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-mnli-xnli"
)


class MDeBERTaMultilingualClassificationModel:
    def __init__(
        self,
        classifier: Callable | None = None,
    ):
        self._classifier = classifier

    def _get_classifier(self):
        if self._classifier is None:
            self._classifier = pipeline(
                "zero-shot-classification",
                model=MODEL_NAME,
                tokenizer=MODEL_NAME,
            )

        return self._classifier

    def predict(
        self,
        text: str,
        candidate_labels: list[str],
    ) -> list[ClassificationPrediction]:
        classifier = self._get_classifier()

        result = classifier(
            text,
            candidate_labels=candidate_labels,
            multi_label=False,
        )

        labels = result.get("labels")
        scores = result.get("scores")

        if (
            not isinstance(labels, list)
            or not isinstance(scores, list)
            or len(labels) != len(scores)
        ):
            raise ModelOutputError(
                "Unexpected zero-shot classification output"
            )

        return [
            ClassificationPrediction(
                label=str(label),
                confidence=round(
                    float(score),
                    4,
                ),
            )
            for label, score in zip(
                labels,
                scores,
            )
        ]
