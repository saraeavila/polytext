from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.api.routes.api_keys import get_api_key_service
from app.core.config import Settings, get_settings
from app.main import app
from app.services.api_key import CreatedAPIKey


class FakeAPIKey:
    def __init__(
        self,
        id: int,
        user_id: int,
        key_prefix: str = "poly_sk_abcdef",
    ):
        self.id = id
        self.user_id = user_id
        self.key_prefix = key_prefix
        self.created_at = datetime(
            2026,
            8,
            13,
            tzinfo=timezone.utc,
        )


class FakeAPIKeyService:
    def create_key(self, user_id: int):
        return CreatedAPIKey(
            api_key=FakeAPIKey(
                id=1,
                user_id=user_id,
            ),
            plaintext_key="poly_sk_fake_plaintext_key",
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_api_key_service] = (
        lambda: FakeAPIKeyService()
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(
        get_api_key_service,
        None,
    )


@pytest.fixture
def admin_auth():
    app.dependency_overrides[
        get_settings
    ] = lambda: Settings(
        polytext_admin_key=SecretStr(
            "test-admin-secret"
        )
    )

    yield

    app.dependency_overrides.pop(
        get_settings,
        None,
    )


def test_create_api_key(
    client,
    admin_auth,
):
    response = client.post(
        "/v1/users/1/keys",
        headers={
            "X-PolyText-Admin-Key": (
                "test-admin-secret"
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == 1
    assert data["key"] == "poly_sk_fake_plaintext_key"


def test_create_api_key_requires_admin(
    client,
    admin_auth,
):
    response = client.post(
        "/v1/users/1/keys"
    )

    assert response.status_code == 401
