from fastapi import APIRouter, Depends, Request

from app.schemas.ner import NERRequest, NERResponse
from app.services.language import LanguageService
from app.services.ner import NERAnalyzer, NERService


router = APIRouter(
    tags=["ner"],
)


def get_ner_service(request: Request) -> NERAnalyzer:
    registry = request.app.state.model_registry
    detector = request.app.state.language_detector

    language_service = LanguageService(
        detector=detector,
    )

    return NERService(
        registry=registry,
        language_service=language_service,
    )


@router.post("/entities", response_model=NERResponse)
def extract_entities(
    request: NERRequest,
    service: NERAnalyzer = Depends(get_ner_service),
) -> NERResponse:
    return service.analyze(request)
