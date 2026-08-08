from app.models.adapters.sentiment.cardiff_multilingual import (
    CardiffMultilingualSentimentModel,
)
from app.models.adapters.sentiment.robertuito_spanish import (
    RobertuitoSpanishSentimentModel,
)
from app.models.adapters.ner.davlan_multilingual import (
    DavlanMultilingualNERModel,
)
from app.models.registry import ModelRegistry


def create_model_registry() -> ModelRegistry:
    registry = ModelRegistry()

    registry.register(
        task="sentiment",
        language="es",
        factory=RobertuitoSpanishSentimentModel,
    )

    registry.register(
        task="sentiment",
        language="*",
        factory=CardiffMultilingualSentimentModel,
    )

    registry.register(
        task="ner",
        language="*",
        factory=DavlanMultilingualNERModel,
    )

    return registry