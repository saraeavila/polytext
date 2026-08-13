import time
from contextlib import contextmanager

from prometheus_client import Counter, Histogram


HTTP_REQUESTS_TOTAL = Counter(
    "polytext_http_requests_total",
    "Total number of HTTP requests",
    [
        "method",
        "route",
        "status",
    ],
)


HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "polytext_http_request_duration_seconds",
    "HTTP request duration in seconds",
    [
        "method",
        "route",
    ],
)


MODEL_RESOLUTIONS_TOTAL = Counter(
    "polytext_model_resolutions_total",
    "Total number of model registry resolutions",
    [
        "task",
        "route",
        "model",
        "load",
    ],
)


MODEL_REQUESTS_TOTAL = Counter(
    "polytext_model_requests_total",
    "Total number of model inference requests",
    [
        "task",
        "model",
    ],
)


MODEL_INFERENCE_DURATION_SECONDS = Histogram(
    "polytext_model_inference_duration_seconds",
    "Model inference duration in seconds",
    [
        "task",
        "model",
    ],
)


RATE_LIMIT_REJECTIONS_TOTAL = Counter(
    "polytext_rate_limit_rejections_total",
    "Total number of requests rejected by rate limiting",
)


@contextmanager
def observe_model_inference(
    task: str,
    model,
):
    model_name = type(model).__name__

    MODEL_REQUESTS_TOTAL.labels(
        task=task,
        model=model_name,
    ).inc()

    start = time.perf_counter()

    try:
        yield

    finally:
        duration_seconds = (
            time.perf_counter() - start
        )

        MODEL_INFERENCE_DURATION_SECONDS.labels(
            task=task,
            model=model_name,
        ).observe(duration_seconds)
