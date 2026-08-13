import pytest

from app.models.adapters.classification.mdeberta_multilingual import (
    MDeBERTaMultilingualClassificationModel,
)
from app.models.errors import ModelOutputError


class FakeClassifier:
    def __call__(
        self,
        text,
        candidate_labels,
        multi_label,
    ):
        return {
            "sequence": text,
            "labels": [
                "technology",
                "finance",
                "sports",
            ],
            "scores": [
                0.812345,
                0.152345,
                0.03531,
            ],
        }


def test_classification_adapter():
    model = (
        MDeBERTaMultilingualClassificationModel(
            classifier=FakeClassifier(),
        )
    )

    predictions = model.predict(
        text="Apple announced a new processor.",
        candidate_labels=[
            "technology",
            "finance",
            "sports",
        ],
    )

    assert len(predictions) == 3

    assert (
        predictions[0].label
        == "technology"
    )

    assert (
        predictions[0].confidence
        == 0.8123
    )


class InvalidFakeClassifier:
    def __call__(
        self,
        text,
        candidate_labels,
        multi_label,
    ):
        return {
            "labels": [
                "technology",
            ],
        }


def test_invalid_output_raises():
    model = (
        MDeBERTaMultilingualClassificationModel(
            classifier=InvalidFakeClassifier(),
        )
    )

    with pytest.raises(ModelOutputError):
        model.predict(
            text="Example",
            candidate_labels=[
                "technology",
                "sports",
            ],
        )
