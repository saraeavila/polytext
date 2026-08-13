from app.models.registry import ModelRegistry
from app.schemas.classification import (
    ClassificationRequest,
    ClassificationResponse,
)
from app.schemas.language import LanguageInfo
from app.services.language import LanguageService


class ClassificationService:
    def __init__(
        self,
        registry: ModelRegistry,
        language_service: LanguageService,
    ):
        self._registry = registry
        self._language_service = (
            language_service
        )

    def classify(
        self,
        request: ClassificationRequest,
    ) -> ClassificationResponse:
        language = (
            self._language_service.resolve(
                text=request.text,
                requested_language=(
                    request.language
                ),
            )
        )

        model = self._registry.get(
            task="classification",
            language=language.routing_language,
        )

        predictions = model.predict(
            text=request.text,
            candidate_labels=(
                request.candidate_labels
            ),
        )

        return ClassificationResponse(
            language=LanguageInfo(
                code=language.code,
                confidence=language.confidence,
            ),
            classification=predictions,
        )
