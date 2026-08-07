from fastapi import APIRouter, Depends

from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.sentiment import SentimentService


router = APIRouter(
    tags=["sentiment"],
)


def get_sentiment_service() -> SentimentService:
    return SentimentService()


@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(
    request: SentimentRequest,
    service: SentimentService = Depends(get_sentiment_service),
) -> SentimentResponse:
    return service.analyze(request)