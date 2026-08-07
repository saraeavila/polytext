from app.models.adapters.sentiment.cardiff_multilingual import (
    CardiffMultilingualSentimentModel,
)
from app.models.registry import ModelRegistry


def create_model_registry() -> ModelRegistry:
    registry = ModelRegistry()

    registry.register(
        task="sentiment",
        language="*",
        factory=CardiffMultilingualSentimentModel,
    )

    return registry