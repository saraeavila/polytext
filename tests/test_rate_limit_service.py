import pytest

from app.services.rate_limit import (
    RateLimitExceededError,
    RateLimitService,
)


class FakeRateLimitRepository:
    def __init__(self, request_count: int):
        self.request_count = request_count

    def count_since(
        self,
        api_key_id,
        since,
    ):
        return self.request_count


def test_request_below_limit_is_allowed():
    repository = FakeRateLimitRepository(
        request_count=4,
    )

    service = RateLimitService(repository)

    service.check(
        api_key_id=1,
        limit_per_minute=5,
    )


def test_request_at_limit_is_rejected():
    repository = FakeRateLimitRepository(
        request_count=5,
    )

    service = RateLimitService(repository)

    with pytest.raises(RateLimitExceededError):
        service.check(
            api_key_id=1,
            limit_per_minute=5,
        )


def test_request_above_limit_is_rejected():
    repository = FakeRateLimitRepository(
        request_count=10,
    )

    service = RateLimitService(repository)

    with pytest.raises(RateLimitExceededError):
        service.check(
            api_key_id=1,
            limit_per_minute=5,
        )
