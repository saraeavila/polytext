from datetime import datetime, timedelta, timezone
from typing import Protocol


class RateLimitRepository(Protocol):
    def count_since(
        self,
        api_key_id: int,
        since: datetime,
    ) -> int:
        ...


class RateLimitExceededError(Exception):
    pass


class RateLimitService:
    def __init__(
        self,
        repository: RateLimitRepository,
    ):
        self._repository = repository

    def check(
        self,
        api_key_id: int,
        limit_per_minute: int,
    ) -> None:
        now = datetime.now(timezone.utc)
        since = now - timedelta(minutes=1)

        request_count = self._repository.count_since(
            api_key_id=api_key_id,
            since=since,
        )

        if request_count >= limit_per_minute:
            raise RateLimitExceededError(
                f"Rate limit of {limit_per_minute} requests per minute exceeded"
            )
