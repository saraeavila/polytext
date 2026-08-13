from collections.abc import Callable
from threading import Lock
from typing import Generic, TypeVar


T = TypeVar("T")


class ThreadSafeLazyLoader(Generic[T]):
    def __init__(
        self,
        factory: Callable[[], T],
        value: T | None = None,
    ):
        self._factory = factory
        self._value = value
        self._lock = Lock()

    def get(self) -> T:
        if self._value is not None:
            return self._value

        with self._lock:
            if self._value is None:
                self._value = self._factory()

        return self._value
