from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.request_usage import RequestUsage


class RequestUsageRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        api_key_id: int,
        request_id: str,
        task: str,
        status_code: int,
        latency_ms: float,
    ) -> RequestUsage:
        usage = RequestUsage(
            api_key_id=api_key_id,
            request_id=request_id,
            task=task,
            status_code=status_code,
            latency_ms=latency_ms,
        )

        self._db.add(usage)
        self._db.commit()
        self._db.refresh(usage)

        return usage

    def get_summary_since(
        self,
        api_key_id: int,
        since: datetime,
    ) -> tuple[int, int, int, float | None]:
        statement = select(
            func.count(RequestUsage.id),
            func.count(RequestUsage.id).filter(
                RequestUsage.status_code < 400
            ),
            func.count(RequestUsage.id).filter(
                RequestUsage.status_code >= 400
            ),
            func.avg(RequestUsage.latency_ms),
        ).where(
            RequestUsage.api_key_id == api_key_id,
            RequestUsage.created_at >= since,
        )

        row = self._db.execute(statement).one()

        total = int(row[0])
        successful = int(row[1])
        failed = int(row[2])
        average_latency = (
            float(row[3])
            if row[3] is not None
            else None
        )

        return (
            total,
            successful,
            failed,
            average_latency,
        )

    def get_task_counts_since(
        self,
        api_key_id: int,
        since: datetime,
    ) -> dict[str, int]:
        statement = (
            select(
                RequestUsage.task,
                func.count(RequestUsage.id),
            )
            .where(
                RequestUsage.api_key_id == api_key_id,
                RequestUsage.created_at >= since,
            )
            .group_by(RequestUsage.task)
        )

        rows = self._db.execute(statement).all()

        return {
            task: int(count)
            for task, count in rows
        }
