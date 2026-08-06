import pytest
from pydantic import ValidationError

from app.schemas.sentiment import (
    SentimentLabel,
    SentimentPrediction,
    SentimentRequest,
)


def test_valid_sentiment_request():
    request = SentimentRequest(
        text="Me encantó este producto.",
        language="es",
    )

    assert request.text == "Me encantó este producto."
    assert request.language == "es"


def test_blank_text_is_rejected():
    with pytest.raises(ValidationError):
        SentimentRequest(
            text="   ",
            language="en",
        )


def test_text_over_max_length_is_rejected():
    with pytest.raises(ValidationError):
        SentimentRequest(
            text="a" * 5001,
            language="en",
        )


def test_language_is_normalized_to_lowercase():
    request = SentimentRequest(
        text="Great product.",
        language="EN",
    )

    assert request.language == "en"


def test_malformed_language_is_rejected():
    with pytest.raises(ValidationError):
        SentimentRequest(
            text="Great product.",
            language="potato!!",
        )


def test_valid_sentiment_label():
    prediction = SentimentPrediction(
        label="positive",
        confidence=0.95,
    )

    assert prediction.label == SentimentLabel.POSITIVE
    assert prediction.confidence == 0.95


def test_unknown_sentiment_label_is_rejected():
    with pytest.raises(ValidationError):
        SentimentPrediction(
            label="happy",
            confidence=0.95,
        )