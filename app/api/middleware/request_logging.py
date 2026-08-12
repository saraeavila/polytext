import logging
import time
import uuid

import anyio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.repositories.request_usage import RequestUsageRepository
from app.services.usage import UsageService


logger = logging.getLogger("polytext.requests")


def persist_usage(
    api_key_id: int,
    request_id: str,
    task: str,
    status_code: int,
    latency_ms: float,
) -> None:
    with SessionLocal() as db:
        repository = RequestUsageRepository(db)
        service = UsageService(repository)

        service.record_request(
            api_key_id=api_key_id,
            request_id=request_id,
            task=task,
            status_code=status_code,
            latency_ms=latency_ms,
        )


async def record_usage_if_needed(
    request: Request,
    request_id: str,
    status_code: int,
    latency_ms: float,
) -> None:
    api_key_id = getattr(
        request.state,
        "api_key_id",
        None,
    )

    task = getattr(
        request.state,
        "usage_task",
        None,
    )

    if api_key_id is None or task is None:
        return

    try:
        await anyio.to_thread.run_sync(
            persist_usage,
            api_key_id,
            request_id,
            task,
            status_code,
            latency_ms,
        )
    except Exception:
        logger.exception(
            "usage_record_failed request_id=%s task=%s",
            request_id,
            task,
        )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        start = time.perf_counter()

        request.state.request_id = request_id

        try:
            response = await call_next(request)

        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000

            await record_usage_if_needed(
                request=request,
                request_id=request_id,
                status_code=500,
                latency_ms=duration_ms,
            )

            logger.exception(
                "request_failed request_id=%s method=%s path=%s duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )

            raise

        duration_ms = (time.perf_counter() - start) * 1000

        await record_usage_if_needed(
            request=request,
            request_id=request_id,
            status_code=response.status_code,
            latency_ms=duration_ms,
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_completed request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
