import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from app.models.lazy import (
    ThreadSafeLazyLoader,
)


def test_lazy_loader_creates_value_once_under_concurrency():
    creation_count = 0
    count_lock = Lock()

    def factory():
        nonlocal creation_count

        with count_lock:
            creation_count += 1

        # Make the race easy to trigger.
        time.sleep(0.05)

        return object()

    loader = ThreadSafeLazyLoader(
        factory=factory
    )

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:
        results = list(
            executor.map(
                lambda _: loader.get(),
                range(5),
            )
        )

    assert creation_count == 1

    assert all(
        result is results[0]
        for result in results
    )
