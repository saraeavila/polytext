from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import app.api.middleware.request_logging as request_logging
from app.api.middleware.request_logging import RequestLoggingMiddleware


def test_authenticated_nlp_request_records_usage(monkeypatch):
    recorded = []

    def fake_persist_usage(
        api_key_id,
        request_id,
        task,
        status_code,
        latency_ms,
    ):
        recorded.append(
            {
                "api_key_id": api_key_id,
                "request_id": request_id,
                "task": task,
                "status_code": status_code,
                "latency_ms": latency_ms,
            }
        )

    monkeypatch.setattr(
        request_logging,
        "persist_usage",
        fake_persist_usage,
    )

    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/test")
    def test_route(request: Request):
        request.state.api_key_id = 42
        request.state.usage_task = "sentiment"

        return {"status": "ok"}

    with TestClient(app) as client:
        response = client.get("/test")

    assert response.status_code == 200

    assert len(recorded) == 1
    assert recorded[0]["api_key_id"] == 42
    assert recorded[0]["task"] == "sentiment"
    assert recorded[0]["status_code"] == 200
    assert recorded[0]["latency_ms"] >= 0

    assert recorded[0]["request_id"] == response.headers["X-Request-ID"]
