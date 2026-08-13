from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_api_key
from app.db.models.api_key import APIKey
from app.db.session import get_db
from app.repositories.request_usage import RequestUsageRepository
from app.services.rate_limit import (
    RateLimitExceededError,
    RateLimitService,
)


def enforce_rate_limit(
    current_key: APIKey = Depends(require_api_key),
    db: Session = Depends(get_db),
) -> APIKey:
    service = RateLimitService(
        repository=RequestUsageRepository(db),
    )

    try:
        service.check(
            api_key_id=current_key.id,
            limit_per_minute=current_key.rate_limit_per_minute,
        )

    except RateLimitExceededError as exc:
        raise HTTPException(
            status_code=429,
            detail=str(exc),
            headers={
                "Retry-After": "60",
            },
        ) from exc

    return current_key
