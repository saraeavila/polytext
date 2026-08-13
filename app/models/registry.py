import logging
from collections.abc import Callable
from typing import Any

from app.core.metrics import (
    MODEL_RESOLUTIONS_TOTAL,
)


logger = logging.getLogger("polytext.models")


class UnsupportedModelError(Exception):
    pass


class ModelRegistry:
    def __init__(self) -> None:
        self._factories: dict[tuple[str, str], Callable[[], Any]] = {}
        self._models: dict[tuple[str, str], Any] = {}

    def register(
        self,
        task: str,
        language: str,
        factory: Callable[[], Any],
    ) -> None:
        key = (task, language)
        self._factories[key] = factory

    def get(self, task: str, language: str) -> Any:
        exact_key = (task, language)
        fallback_key = (task, "*")

        if exact_key in self._factories:
            key = exact_key
            route = "exact"
        elif fallback_key in self._factories:
            key = fallback_key
            route = "fallback"
        else:
            raise UnsupportedModelError(
                f"No model available for task={task!r}, language={language!r}"
            )

        if key not in self._models:
            model = self._factories[key]()
            self._models[key] = model
            load = "cold"
        else:
            model = self._models[key]
            load = "reused"

        MODEL_RESOLUTIONS_TOTAL.labels(
            task=task,
            route=route,
            model=type(model).__name__,
            load=load,
        ).inc()

        logger.info(
            "model_resolved task=%s language=%s route=%s model=%s load=%s",
            task,
            language,
            route,
            type(model).__name__,
            load,
        )

        return model