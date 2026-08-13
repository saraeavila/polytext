from datetime import datetime, timedelta, timezone
from typing import Protocol

from app.schemas.usage import (
    TaskUsage,
    UsageSummaryResponse,
)


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

    def get_summary_since(
        self,
        api_key_id: int,
        since: datetime,
    ):
        ...

    def get_task_counts_since(
        self,
        api_key_id: int,
        since: datetime,
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

    def get_summary(
        self,
        api_key_id: int,
        hours: int,
    ) -> UsageSummaryResponse:
        since = datetime.now(timezone.utc) - timedelta(
            hours=hours
        )

        (
            total,
            successful,
            failed,
            average_latency,
        ) = self._repository.get_summary_since(
            api_key_id=api_key_id,
            since=since,
        )

        task_counts = self._repository.get_task_counts_since(
            api_key_id=api_key_id,
            since=since,
        )

        return UsageSummaryResponse(
            api_key_id=api_key_id,
            period_hours=hours,
            total_requests=total,
            successful_requests=successful,
            failed_requests=failed,
            average_latency_ms=(
                round(average_latency, 2)
                if average_latency is not None
                else None
            ),
            tasks=[
                TaskUsage(
                    task=task,
                    requests=count,
                )
                for task, count in sorted(
                    task_counts.items()
                )
            ],
        )
