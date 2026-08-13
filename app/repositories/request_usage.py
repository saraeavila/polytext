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

    def count_since(
        self,
        api_key_id: int,
        since: datetime,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(RequestUsage)
            .where(
                RequestUsage.api_key_id == api_key_id,
                RequestUsage.created_at >= since,
            )
        )

        return self._db.scalar(statement) or 0
