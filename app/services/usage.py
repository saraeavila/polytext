from typing import Protocol


class UsageRepository(Protocol):
    def create(
        self,
        api_key_id: int,
        request_id: str,
        task: str,
        status_code: int,
        latency_ms: float,
    ):
        ...


class UsageService:
    def __init__(self, repository: UsageRepository):
        self._repository = repository

    def record_request(
        self,
        api_key_id: int,
        request_id: str,
        task: str,
        status_code: int,
        latency_ms: float,
    ):
        return self._repository.create(
            api_key_id=api_key_id,
            request_id=request_id,
            task=task,
            status_code=status_code,
            latency_ms=latency_ms,
        )
