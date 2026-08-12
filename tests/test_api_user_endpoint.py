from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.routes.api_users import get_api_user_service
from app.main import app
from app.services.api_user import APIUserAlreadyExistsError


class FakeUser:
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = datetime(
            2026,
            8,
            11,
            tzinfo=timezone.utc,
        )


class FakeAPIUserService:
    def create_user(self, name: str, email: str):
        return FakeUser(
            id=1,
            name=name,
            email=email,
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_api_user_service] = (
        lambda: FakeAPIUserService()
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(
        get_api_user_service,
        None,
    )


def test_create_api_user(client):
    response = client.post(
        "/v1/users",
        json={
            "name": "Sara",
            "email": "sara@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Sara"
    assert data["email"] == "sara@example.com"


def test_invalid_email_is_rejected(client):
    response = client.post(
        "/v1/users",
        json={
            "name": "Sara",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422


class DuplicateAPIUserService:
    def create_user(self, name: str, email: str):
        raise APIUserAlreadyExistsError(
            f"API user with email {email!r} already exists"
        )


def test_duplicate_user_returns_409():
    app.dependency_overrides[get_api_user_service] = (
        lambda: DuplicateAPIUserService()
    )

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/users",
                json={
                    "name": "Sara",
                    "email": "sara@example.com",
                },
            )

        assert response.status_code == 409

    finally:
        app.dependency_overrides.pop(
            get_api_user_service,
            None,
        )
