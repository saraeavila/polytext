from typing import Protocol

from app.domain.classification import (
    ClassificationPrediction,
)


class ClassificationModel(Protocol):
    def predict(
        self,
        text: str,
        candidate_labels: list[str],
    ) -> list[ClassificationPrediction]:
        ...
