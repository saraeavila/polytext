from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.errors import register_exception_handlers
from app.models.errors import ModelOutputError
from app.models.registry import UnsupportedModelError


def create_test_app() -> FastAPI:
    app = FastAPI()

    register_exception_handlers(app)

    @app.get("/unsupported")
    def raise_unsupported():
        raise UnsupportedModelError(
            "No model available for task='test', language='xx'"
        )

    @app.get("/bad-output")
    def raise_bad_output():
        raise ModelOutputError("Unexpected label")

    return app


def test_unsupported_model_returns_structured_error():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/unsupported")

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "unsupported_model",
            "message": "No model available for task='test', language='xx'",
        }
    }


def test_model_output_error_returns_safe_message():
    app = create_test_app()

    with TestClient(app) as client:
        response = client.get("/bad-output")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "model_output_error",
            "message": "The model returned an unexpected result.",
        }
    }
