from pydantic import BaseModel, Field, field_validator


class LanguageInfo(BaseModel):
    code: str = Field(
        pattern=r"^[a-z]{2,3}(?:-[a-z]{2,4})?$"
    )
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    @field_validator("code", mode="before")
    @classmethod
    def normalize_code(cls, value):
        if isinstance(value, str):
            return value.lower()

        return value
