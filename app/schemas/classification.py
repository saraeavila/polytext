from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from app.domain.classification import (
    ClassificationPrediction,
)
from app.schemas.language import LanguageInfo


class ClassificationRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
    )

    candidate_labels: list[str] = Field(
        min_length=2,
        max_length=20,
    )

    language: str | None = Field(
        default=None,
        pattern=r"^[a-z]{2,3}(?:-[a-z]{2,4})?$",
    )

    @field_validator("text")
    @classmethod
    def reject_whitespace_only_text(
        cls,
        value: str,
    ) -> str:
        if not value.strip():
            raise ValueError(
                "text must not be blank"
            )

        return value

    @field_validator("candidate_labels")
    @classmethod
    def validate_candidate_labels(
        cls,
        labels: list[str],
    ) -> list[str]:
        cleaned = [
            label.strip()
            for label in labels
        ]

        if any(not label for label in cleaned):
            raise ValueError(
                "candidate labels must not be blank"
            )

        if any(
            len(label) > 100
            for label in cleaned
        ):
            raise ValueError(
                "candidate labels must be at most 100 characters"
            )

        normalized = [
            label.casefold()
            for label in cleaned
        ]

        if len(normalized) != len(set(normalized)):
            raise ValueError(
                "candidate labels must be unique"
            )

        return cleaned

    @field_validator(
        "language",
        mode="before",
    )
    @classmethod
    def normalize_language(
        cls,
        value,
    ):
        if isinstance(value, str):
            return value.lower()

        return value


class ClassificationResponse(BaseModel):
    language: LanguageInfo
    classification: list[
        ClassificationPrediction
    ]
