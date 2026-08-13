import pytest

from app.repositories.redis_rate_limit import (
    RedisRateLimitRepository,
)


pytestmark = pytest.mark.integration


def test_redis_rate_limit_counter(
    redis_client,
):
    repository = RedisRateLimitRepository(
        client=redis_client,
        window_seconds=60,
    )

    first_count, first_ttl = (
        repository.increment(
            api_key_id=123,
        )
    )

    assert first_count == 1
    assert 1 <= first_ttl <= 60

    second_count, second_ttl = (
        repository.increment(
            api_key_id=123,
        )
    )

    assert second_count == 2
    assert 1 <= second_ttl <= 60


def test_different_api_keys_have_separate_counters(
    redis_client,
):
    repository = RedisRateLimitRepository(
        client=redis_client,
        window_seconds=60,
    )

    first_key_count, _ = (
        repository.increment(
            api_key_id=1,
        )
    )

    second_key_count, _ = (
        repository.increment(
            api_key_id=2,
        )
    )

    assert first_key_count == 1
    assert second_key_count == 1


def test_redis_is_reachable(
    redis_client,
):
    assert redis_client.ping() is True
