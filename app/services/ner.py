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
        language = self._language_service.resolve(
            text=request.text,
            requested_language=request.language,
        )

        model = self._registry.get(
            task="ner",
            language=language.routing_language,
        )

        entities = model.predict(request.text)

        return NERResponse(
            language=LanguageInfo(
                code=language.code,
                confidence=language.confidence,
            ),
            entities=entities,
        )
