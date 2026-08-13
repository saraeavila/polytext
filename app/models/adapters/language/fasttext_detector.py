from pathlib import Path
from typing import Protocol

import fasttext

from app.core.config import get_settings
from app.domain.language import LanguagePrediction


class FastTextModel(Protocol):
    def predict(self, text: str, k: int = 1):
        ...


class FastTextLanguageDetector:
    def __init__(
        self,
        model: FastTextModel | None = None,
        model_path: str | None = None,
    ) -> None:
        self._model = model

        if model is None:
            if model_path is None:
                model_path = (
                    get_settings()
                    .fasttext_model_path
                )

            model_path = Path(model_path)

            if not model_path.exists():
                raise FileNotFoundError(
                    f"Language model not found at {model_path}"
                )

            self._model = fasttext.load_model(str(model_path))

    def detect(self, text: str) -> LanguagePrediction:
        normalized_text = text.replace("\n", " ")

        labels, probabilities = self._model.predict(
            normalized_text,
            k=1,
        )

        raw_label = labels[0]
        confidence = float(probabilities[0])

        code = raw_label.removeprefix("__label__")

        return LanguagePrediction(
            code=code,
            confidence=round(confidence, 4),
        )
