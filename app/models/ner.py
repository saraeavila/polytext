from typing import Protocol

from app.domain.ner import EntityPrediction


class NERModel(Protocol):
    def predict(self, text: str) -> list[EntityPrediction]:
        ...


class PlaceholderNERModel:
    def predict(self, text: str) -> list[EntityPrediction]:
        return []
