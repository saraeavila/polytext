import pytest

from app.domain.sentiment import SentimentLabel
from app.models.adapters.sentiment.cardiff_multilingual import (
    CardiffMultilingualSentimentModel,
)
from app.models.errors import ModelOutputError


class FakeClassifier:
    def __init__(self, label: str, score: float):
        self.label = label
        self.score = score

    def __call__(self, text: str, **kwargs):
        return [
            {
                "label": self.label,
                "score": self.score,
            }
        ]


def test_adapter_maps_positive_label():
    model = CardiffMultilingualSentimentModel(
        classifier=FakeClassifier(
            label="positive",
            score=0.947973370552063,
        )
    )

    result = model.predict("Great product.")

    assert result.label == SentimentLabel.POSITIVE
    assert result.confidence == 0.948


def test_adapter_maps_negative_label():
    model = CardiffMultilingualSentimentModel(
        classifier=FakeClassifier(
            label="negative",
            score=0.91,
        )
    )

    result = model.predict("Terrible product.")

    assert result.label == SentimentLabel.NEGATIVE


def test_adapter_maps_neutral_label():
    model = CardiffMultilingualSentimentModel(
        classifier=FakeClassifier(
            label="neutral",
            score=0.72,
        )
    )

    result = model.predict("It was okay.")

    assert result.label == SentimentLabel.NEUTRAL


def test_adapter_normalizes_label_case():
    model = CardiffMultilingualSentimentModel(
        classifier=FakeClassifier(
            label="POSITIVE",
            score=0.88,
        )
    )

    result = model.predict("Great.")

    assert result.label == SentimentLabel.POSITIVE


def test_adapter_raises_for_unknown_label():
    model = CardiffMultilingualSentimentModel(
        classifier=FakeClassifier(
            label="LABEL_7",
            score=0.9,
        )
    )

    with pytest.raises(ModelOutputError):
        model.predict("Something.")