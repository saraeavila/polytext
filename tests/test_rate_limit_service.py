import pytest

from app.services.rate_limit import (
    RateLimitExceededError,
    RateLimitService,
)


class FakeRateLimitRepository:
    def __init__(
        self,
        count: int,
        ttl: int = 60,
    ):
        self.count = count
        self.ttl = ttl

    def increment(
        self,
        api_key_id: int,
    ) -> tuple[int, int]:
        return self.count, self.ttl


def test_request_below_limit_is_allowed():
    service = RateLimitService(
        FakeRateLimitRepository(
            count=4,
        )
    )

    service.check(
        api_key_id=1,
        limit_per_minute=5,
    )


def test_request_at_limit_is_allowed():
    service = RateLimitService(
        FakeRateLimitRepository(
            count=5,
        )
    )

    service.check(
        api_key_id=1,
        limit_per_minute=5,
    )


def test_request_above_limit_is_rejected():
    service = RateLimitService(
        FakeRateLimitRepository(
            count=6,
            ttl=37,
        )
    )

    with pytest.raises(
        RateLimitExceededError
    ) as exc_info:
        service.check(
            api_key_id=1,
            limit_per_minute=5,
        )

    assert (
        exc_info.value.retry_after_seconds
        == 37
    )
