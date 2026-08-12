from fastapi import APIRouter, Depends, Request

from app.api.dependencies.auth import require_api_key
from app.api.dependencies.usage import mark_sentiment_usage
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.language import LanguageService
from app.services.sentiment import SentimentAnalyzer, SentimentService


router = APIRouter(
    tags=["sentiment"],
)


def get_sentiment_service(request: Request) -> SentimentAnalyzer:
    registry = request.app.state.model_registry
    detector = request.app.state.language_detector

    language_service = LanguageService(
        detector=detector,
    )

    return SentimentService(
        registry=registry,
        language_service=language_service,
    )


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    dependencies=[
        Depends(require_api_key),
        Depends(mark_sentiment_usage),
    ],
)
def analyze_sentiment(
    request: SentimentRequest,
    service: SentimentService = Depends(get_sentiment_service),
) -> SentimentResponse:
    return service.analyze(request)