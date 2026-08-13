import app.models.setup as setup
from app.models.adapters.classification.mdeberta_multilingual import (
    MDeBERTaMultilingualClassificationModel,
)


class FakeSpanishModel:
    pass


class FakeMultilingualModel:
    pass


def test_spanish_routes_to_specialist(monkeypatch):
    monkeypatch.setattr(
        setup,
        "RobertuitoSpanishSentimentModel",
        FakeSpanishModel,
    )
    monkeypatch.setattr(
        setup,
        "CardiffMultilingualSentimentModel",
        FakeMultilingualModel,
    )

    registry = setup.create_model_registry()

    model = registry.get("sentiment", "es")

    assert isinstance(model, FakeSpanishModel)


def test_english_routes_to_multilingual_fallback(monkeypatch):
    monkeypatch.setattr(
        setup,
        "RobertuitoSpanishSentimentModel",
        FakeSpanishModel,
    )
    monkeypatch.setattr(
        setup,
        "CardiffMultilingualSentimentModel",
        FakeMultilingualModel,
    )

    registry = setup.create_model_registry()

    model = registry.get("sentiment", "en")

    assert isinstance(model, FakeMultilingualModel)


def test_portuguese_routes_to_multilingual_fallback(monkeypatch):
    monkeypatch.setattr(
        setup,
        "RobertuitoSpanishSentimentModel",
        FakeSpanishModel,
    )
    monkeypatch.setattr(
        setup,
        "CardiffMultilingualSentimentModel",
        FakeMultilingualModel,
    )

    registry = setup.create_model_registry()

    model = registry.get("sentiment", "pt")

    assert isinstance(model, FakeMultilingualModel)


def test_classification_model_is_registered():
    registry = setup.create_model_registry()

    model = registry.get(
        task="classification",
        language="en",
    )

    assert isinstance(
        model,
        MDeBERTaMultilingualClassificationModel,
    )