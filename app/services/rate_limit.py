from typing import Protocol


class RateLimitRepository(Protocol):
    def increment(
        self,
        api_key_id: int,
    ) -> tuple[int, int]:
        ...


class RateLimitExceededError(Exception):
    def __init__(
        self,
        limit_per_minute: int,
        retry_after_seconds: int,
    ):
        self.retry_after_seconds = retry_after_seconds

        super().__init__(
            f"Rate limit of "
            f"{limit_per_minute} requests per minute exceeded"
        )


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
        count, retry_after = self._repository.increment(
            api_key_id=api_key_id,
        )

        if count > limit_per_minute:
            raise RateLimitExceededError(
                limit_per_minute=limit_per_minute,
                retry_after_seconds=retry_after,
            )
