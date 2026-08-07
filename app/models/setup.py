from app.models.registry import ModelRegistry
from app.models.sentiment import PlaceholderSentimentModel


def create_model_registry() -> ModelRegistry:
    registry = ModelRegistry()

    registry.register(
        task="sentiment",
        language="*",
        factory=PlaceholderSentimentModel,
    )

    return registry