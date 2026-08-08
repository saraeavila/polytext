import pytest
from pydantic import ValidationError

from app.domain.ner import EntityLabel, EntityPrediction
from app.schemas.ner import NERRequest


def test_valid_ner_request():
    request = NERRequest(
        text="Sara visited Madrid.",
        language="EN",
    )

    assert request.language == "en"


def test_ner_request_allows_automatic_language_detection():
    request = NERRequest(
        text="Sara visitó Madrid."
    )

    assert request.language is None


def test_blank_ner_text_is_rejected():
    with pytest.raises(ValidationError):
        NERRequest(
            text="   ",
            language="en",
        )


def test_valid_entity_prediction():
    entity = EntityPrediction(
        text="Madrid",
        label="location",
        start=13,
        end=19,
        confidence=0.96,
    )

    assert entity.label == EntityLabel.LOCATION
    assert entity.text == "Madrid"


def test_unknown_entity_label_is_rejected():
    with pytest.raises(ValidationError):
        EntityPrediction(
            text="Madrid",
            label="CITY",
            start=13,
            end=19,
            confidence=0.96,
        )
