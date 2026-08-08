from typing import Protocol

from app.models.registry import ModelRegistry
from app.schemas.language import LanguageInfo
from app.schemas.ner import NERRequest, NERResponse
from app.services.language import LanguageService


class NERAnalyzer(Protocol):
    def analyze(self, request: NERRequest) -> NERResponse:
        ...


class NERService:
    def __init__(
        self,
        registry: ModelRegistry,
        language_service: LanguageService,
    ):
        self._registry = registry
        self._language_service = language_service

    def analyze(self, request: NERRequest) -> NERResponse:
        if request.language is not None:
            routing_language = request.language

            language = LanguageInfo(
                code=request.language,
                confidence=None,
            )

        else:
            detected = self._language_service.detect(request.text)

            routing_language = self._language_service.routing_language(
                detected
            )

            language = LanguageInfo(
                code=detected.code,
                confidence=detected.confidence,
            )

        model = self._registry.get(
            task="ner",
            language=routing_language,
        )

        entities = model.predict(request.text)

        return NERResponse(
            language=language,
            entities=entities,
        )
