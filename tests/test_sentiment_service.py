from app.domain.sentiment import SentimentLabel, SentimentPrediction
from app.schemas.sentiment import SentimentRequest
from app.services.sentiment import SentimentService


class FakeSentimentModel:
    def predict(self, text: str) -> SentimentPrediction:
        return SentimentPrediction(
            label=SentimentLabel.POSITIVE,
            confidence=0.91,
        )


def test_sentiment_service_uses_model_prediction():
    service = SentimentService(model=FakeSentimentModel())

    request = SentimentRequest(
        text="Me encantó.",
        language="es",
    )

    result = service.analyze(request)

    assert result.language == "es"
    assert result.sentiment.label == SentimentLabel.POSITIVE
    assert result.sentiment.confidence == 0.91