from enum import Enum

from pydantic import BaseModel, Field


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentPrediction(BaseModel):
    label: SentimentLabel
    confidence: float = Field(ge=0.0, le=1.0)
