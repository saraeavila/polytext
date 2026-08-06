from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

    language: str = Field(
        pattern=r"^[a-z]{2,3}(?:-[a-z]{2,4})?$"
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be blank")

        return value

    @field_validator("language", mode="before")
    @classmethod
    def normalize_language(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()

        return value


class SentimentPrediction(BaseModel):
    label: SentimentLabel
    confidence: float = Field(ge=0.0, le=1.0)


class SentimentResponse(BaseModel):
    language: str
    sentiment: SentimentPrediction