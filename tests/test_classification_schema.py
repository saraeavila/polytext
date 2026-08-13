import pytest
from pydantic import ValidationError

from app.schemas.classification import (
    ClassificationRequest,
)


def test_classification_request():
    request = ClassificationRequest(
        text="Apple released a new processor.",
        candidate_labels=[
            "technology",
            "sports",
            "politics",
        ],
        language="en",
    )

    assert request.text == (
        "Apple released a new processor."
    )

    assert request.candidate_labels == [
        "technology",
        "sports",
        "politics",
    ]

    assert request.language == "en"


def test_language_is_normalized():
    request = ClassificationRequest(
        text="Hola mundo.",
        candidate_labels=[
            "tecnología",
            "deportes",
        ],
        language="ES",
    )

    assert request.language == "es"


def test_requires_at_least_two_labels():
    with pytest.raises(ValidationError):
        ClassificationRequest(
            text="Example",
            candidate_labels=[
                "technology",
            ],
        )


def test_duplicate_labels_are_rejected():
    with pytest.raises(ValidationError):
        ClassificationRequest(
            text="Example",
            candidate_labels=[
                "Technology",
                "technology",
            ],
        )


def test_blank_label_is_rejected():
    with pytest.raises(ValidationError):
        ClassificationRequest(
            text="Example",
            candidate_labels=[
                "technology",
                "   ",
            ],
        )
