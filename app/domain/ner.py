from enum import Enum

from pydantic import BaseModel, Field


class EntityLabel(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    MISCELLANEOUS = "miscellaneous"


class EntityPrediction(BaseModel):
    text: str
    label: EntityLabel
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    confidence: float = Field(ge=0.0, le=1.0)
