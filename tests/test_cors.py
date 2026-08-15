from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi.testclient import TestClient


def create_cors_test_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://frontend.example.com",
        ],
        allow_credentials=False,
        allow_methods=[
            "GET",
            "POST",
        ],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-PolyText-Admin-Key",
        ],
        expose_headers=[
            "X-Request-ID",
        ],
    )

    @app.get("/test")
    def test_route():
        return {
            "status": "ok",
        }

    return app


def test_allowed_cors_origin():
    app = create_cors_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/test",
            headers={
                "Origin": (
                    "https://frontend.example.com"
                ),
            },
        )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "https://frontend.example.com"
    )


def test_unapproved_cors_origin_not_allowed():
    app = create_cors_test_app()

    with TestClient(app) as client:
        response = client.get(
            "/test",
            headers={
                "Origin": (
                    "https://evil.example.com"
                ),
            },
        )

    assert response.status_code == 200

    assert (
        "access-control-allow-origin"
        not in response.headers
    )
