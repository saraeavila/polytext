from pydantic import BaseModel, Field


class LanguagePrediction(BaseModel):
    code: str
    confidence: float = Field(ge=0.0, le=1.0)