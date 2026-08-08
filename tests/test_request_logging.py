from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.middleware.request_logging import RequestLoggingMiddleware


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/test")
    def test_route():
        return {"status": "ok"}

    return app


def test_request_gets_request_id_header():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/test")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_each_request_gets_unique_request_id():
    app = create_test_app()

    with TestClient(app) as client:
        first = client.get("/test")
        second = client.get("/test")

    assert first.headers["X-Request-ID"] != second.headers["X-Request-ID"]
