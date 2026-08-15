import pytest

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.api.dependencies.admin import (
    require_admin_key,
)
from app.core.config import (
    Settings,
    get_settings,
)


admin_test_app = FastAPI()


@admin_test_app.get(
    "/admin-test",
    dependencies=[
        Depends(require_admin_key),
    ],
)
def admin_test():
    return {
        "status": "ok",
    }


@pytest.fixture
def client():
    def override_settings():
        return Settings(
            polytext_admin_key=SecretStr(
                "test-admin-secret"
            )
        )

    admin_test_app.dependency_overrides[
        get_settings
    ] = override_settings

    with TestClient(
        admin_test_app
    ) as test_client:
        yield test_client

    admin_test_app.dependency_overrides.pop(
        get_settings,
        None,
    )


def test_admin_key_allows_access(
    client,
):
    response = client.get(
        "/admin-test",
        headers={
            "X-PolyText-Admin-Key": (
                "test-admin-secret"
            )
        },
    )

    assert response.status_code == 200


def test_missing_admin_key_is_rejected(
    client,
):
    response = client.get(
        "/admin-test"
    )

    assert response.status_code == 401


def test_invalid_admin_key_is_rejected(
    client,
):
    response = client.get(
        "/admin-test",
        headers={
            "X-PolyText-Admin-Key": (
                "wrong-secret"
            )
        },
    )

    assert response.status_code == 401


def test_missing_admin_configuration_returns_503():
    app = FastAPI()

    @app.get(
        "/admin-test",
        dependencies=[
            Depends(require_admin_key),
        ],
    )
    def admin_test():
        return {
            "status": "ok",
        }

    app.dependency_overrides[
        get_settings
    ] = lambda: Settings(
        polytext_admin_key=None
    )

    with TestClient(app) as client:
        response = client.get(
            "/admin-test",
            headers={
                "X-PolyText-Admin-Key": (
                    "anything"
                )
            },
        )

    assert response.status_code == 503
