import pytest

from app.models.registry import ModelRegistry, UnsupportedModelError


class FakeModel:
    def __init__(self, name: str):
        self.name = name


def test_registry_uses_exact_language_match():
    registry = ModelRegistry()

    registry.register(
        "sentiment",
        "es",
        lambda: FakeModel("spanish-specialist"),
    )

    registry.register(
        "sentiment",
        "*",
        lambda: FakeModel("multilingual-fallback"),
    )

    model = registry.get("sentiment", "es")

    assert model.name == "spanish-specialist"


def test_registry_uses_fallback_when_exact_match_missing():
    registry = ModelRegistry()

    registry.register(
        "sentiment",
        "*",
        lambda: FakeModel("multilingual-fallback"),
    )

    model = registry.get("sentiment", "pt")

    assert model.name == "multilingual-fallback"


def test_registry_raises_when_no_model_exists():
    registry = ModelRegistry()

    with pytest.raises(UnsupportedModelError):
        registry.get("sentiment", "es")


def test_registry_lazy_loads_model():
    registry = ModelRegistry()
    load_count = 0

    def factory():
        nonlocal load_count
        load_count += 1
        return FakeModel("spanish-specialist")

    registry.register("sentiment", "es", factory)

    assert load_count == 0

    registry.get("sentiment", "es")

    assert load_count == 1


def test_registry_reuses_loaded_model():
    registry = ModelRegistry()
    load_count = 0

    def factory():
        nonlocal load_count
        load_count += 1
        return FakeModel("spanish-specialist")

    registry.register("sentiment", "es", factory)

    first_model = registry.get("sentiment", "es")
    second_model = registry.get("sentiment", "es")

    assert first_model is second_model
    assert load_count == 1