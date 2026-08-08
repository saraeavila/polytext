import pytest

from app.domain.sentiment import SentimentLabel
from app.models.adapters.sentiment.robertuito_spanish import (
    RobertuitoSpanishSentimentModel,
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
    model = RobertuitoSpanishSentimentModel(
        classifier=FakeClassifier("POS", 0.93456)
    )

    result = model.predict("Me encantó.")

    assert result.label == SentimentLabel.POSITIVE
    assert result.confidence == 0.9346


def test_adapter_maps_negative_label():
    model = RobertuitoSpanishSentimentModel(
        classifier=FakeClassifier("NEG", 0.91)
    )

    result = model.predict("Fue terrible.")

    assert result.label == SentimentLabel.NEGATIVE


def test_adapter_maps_neutral_label():
    model = RobertuitoSpanishSentimentModel(
        classifier=FakeClassifier("NEU", 0.75)
    )

    result = model.predict("Estuvo normal.")

    assert result.label == SentimentLabel.NEUTRAL


def test_adapter_raises_for_unknown_label():
    model = RobertuitoSpanishSentimentModel(
        classifier=FakeClassifier("UNKNOWN", 0.9)
    )

    with pytest.raises(ModelOutputError):
        model.predict("Texto.")