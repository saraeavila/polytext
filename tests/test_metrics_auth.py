import pytest

from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.core.config import (
    Settings,
    get_settings,
)
from app.main import app


@pytest.fixture
def production_settings():
    app.dependency_overrides[
        get_settings
    ] = lambda: Settings(
        environment="production",
        polytext_admin_key=SecretStr(
            "test-admin-secret"
        ),
    )

    yield

    app.dependency_overrides.pop(
        get_settings,
        None,
    )


def test_metrics_requires_auth_in_production(
    production_settings,
):
    with TestClient(app) as client:
        response = client.get(
            "/metrics"
        )

    assert response.status_code == 401


def test_metrics_accepts_admin_key_in_production(
    production_settings,
):
    with TestClient(app) as client:
        response = client.get(
            "/metrics",
            headers={
                "X-PolyText-Admin-Key": (
                    "test-admin-secret"
                )
            },
        )

    assert response.status_code == 200

    assert (
        "polytext_http_requests_total"
        in response.text
    )
