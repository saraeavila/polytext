from fastapi import Depends, HTTPException

from app.api.dependencies.auth import require_api_key
from app.core.redis import redis_client
from app.db.models.api_key import APIKey
from app.repositories.redis_rate_limit import (
    RedisRateLimitRepository,
)
from app.services.rate_limit import (
    RateLimitExceededError,
    RateLimitService,
)


def enforce_rate_limit(
    current_key: APIKey = Depends(require_api_key),
) -> APIKey:
    service = RateLimitService(
        repository=RedisRateLimitRepository(
            redis_client
        ),
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
                "Retry-After": str(
                    exc.retry_after_seconds
                ),
            },
        ) from exc

    return current_key
