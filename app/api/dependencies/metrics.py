from hmac import compare_digest
from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import APIKeyHeader

from app.core.config import (
    Settings,
    get_settings,
)


metrics_key_header = APIKeyHeader(
    name="X-PolyText-Admin-Key",
    auto_error=False,
)


def require_metrics_access(
    provided_key: Annotated[
        str | None,
        Depends(metrics_key_header),
    ],
    settings: Annotated[
        Settings,
        Depends(get_settings),
    ],
) -> None:
    if not settings.is_production:
        return

    configured_key = (
        settings.polytext_admin_key
    )

    if configured_key is None:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "Metrics authentication "
                "is not configured."
            ),
        )

    expected_key = (
        configured_key.get_secret_value()
    )

    if (
        provided_key is None
        or not compare_digest(
            provided_key,
            expected_key,
        )
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="Invalid metrics credentials.",
        )
