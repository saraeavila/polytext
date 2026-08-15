import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.readiness import (
    check_postgres,
    check_redis,
)


logger = logging.getLogger(
    "polytext.readiness"
)

router = APIRouter()


@router.get("/ready")
def readiness():
    checks = {
        "postgres": "ready",
        "redis": "ready",
    }

    try:
        check_postgres()

    except Exception:
        checks["postgres"] = "unavailable"

        logger.warning(
            "readiness_check_failed "
            "dependency=postgres",
            exc_info=True,
        )

    try:
        check_redis()

    except Exception:
        checks["redis"] = "unavailable"

        logger.warning(
            "readiness_check_failed "
            "dependency=redis",
            exc_info=True,
        )

    is_ready = all(
        value == "ready"
        for value in checks.values()
    )

    if not is_ready:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": checks,
            },
        )

    return {
        "status": "ready",
        "checks": checks,
    }
