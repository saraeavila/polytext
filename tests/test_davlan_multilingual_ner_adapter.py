import pytest

from app.domain.ner import EntityLabel
from app.models.adapters.ner.davlan_multilingual import (
    DavlanMultilingualNERModel,
)
from app.models.errors import ModelOutputError


class FakeClassifier:
    def __init__(self, results):
        self.results = results

    def __call__(self, text: str, **kwargs):
        return self.results


def test_adapter_maps_person_entity():
    text = "Sara visited Madrid."

    model = DavlanMultilingualNERModel(
        classifier=FakeClassifier(
            [
                {
                    "entity_group": "PER",
                    "score": 0.987654,
                    "start": 0,
                    "end": 4,
                }
            ]
        )
    )

    result = model.predict(text)

    assert len(result) == 1
    assert result[0].text == "Sara"
    assert result[0].label == EntityLabel.PERSON
    assert result[0].confidence == 0.9877


def test_adapter_maps_location_entity():
    text = "Sara visited Madrid."

    model = DavlanMultilingualNERModel(
        classifier=FakeClassifier(
            [
                {
                    "entity_group": "LOC",
                    "score": 0.96,
                    "start": 13,
                    "end": 19,
                }
            ]
        )
    )

    result = model.predict(text)

    assert result[0].text == "Madrid"
    assert result[0].label == EntityLabel.LOCATION


def test_adapter_maps_organization_entity():
    text = "Sara works at Microsoft."

    model = DavlanMultilingualNERModel(
        classifier=FakeClassifier(
            [
                {
                    "entity_group": "ORG",
                    "score": 0.94,
                    "start": 14,
                    "end": 23,
                }
            ]
        )
    )

    result = model.predict(text)

    assert result[0].text == "Microsoft"
    assert result[0].label == EntityLabel.ORGANIZATION


def test_adapter_raises_for_unknown_label():
    model = DavlanMultilingualNERModel(
        classifier=FakeClassifier(
            [
                {
                    "entity_group": "EVENT",
                    "score": 0.90,
                    "start": 0,
                    "end": 4,
                }
            ]
        )
    )

    with pytest.raises(ModelOutputError):
        model.predict("Test")
