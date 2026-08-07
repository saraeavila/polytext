from app.schemas.sentiment import (
    SentimentLabel,
    SentimentPrediction,
    SentimentRequest,
    SentimentResponse,
)


class SentimentService:
    def analyze(self, request: SentimentRequest) -> SentimentResponse:
        return SentimentResponse(
            language=request.language,
            sentiment=SentimentPrediction(
                label=SentimentLabel.NEUTRAL,
                confidence=1.0,
            ),
        )