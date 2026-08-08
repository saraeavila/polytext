import pytest
from pydantic import ValidationError

from app.domain.language import LanguagePrediction


def test_language_code_is_normalized():
    prediction = LanguagePrediction(
        code="ES",
        confidence=0.98,
    )

    assert prediction.code == "es"


def test_invalid_language_code_is_rejected():
    with pytest.raises(ValidationError):
        LanguagePrediction(
            code="potato!!",
            confidence=0.98,
        )