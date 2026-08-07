from collections.abc import Callable
from typing import Any


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
        elif fallback_key in self._factories:
            key = fallback_key
        else:
            raise UnsupportedModelError(
                f"No model available for task={task!r}, language={language!r}"
            )

        if key not in self._models:
            self._models[key] = self._factories[key]()

        return self._models[key]