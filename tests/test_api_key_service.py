from datetime import datetime, timezone

import pytest

from app.services.api_key import (
    APIKeyForbiddenError,
    APIKeyNotFoundError,
    APIKeyService,
)


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
        self.key_hash = f"hash-{id}"
        self.revoked_at = None


class FakeAPIKeyRepository:
    def __init__(self):
        self.keys = {}

    def get_by_id(self, api_key_id: int):
        return self.keys.get(api_key_id)

    def revoke(self, api_key):
        if api_key.revoked_at is None:
            api_key.revoked_at = datetime.now(timezone.utc)

        return api_key


@pytest.fixture
def repository():
    return FakeAPIKeyRepository()


@pytest.fixture
def service(repository):
    return APIKeyService(
        repository=repository,
        user_repository=None,
    )


def test_user_can_revoke_own_key(repository, service):
    api_key = FakeAPIKey(id=1, user_id=42)
    repository.keys[1] = api_key

    revoked = service.revoke_key(
        api_key_id=1,
        requesting_user_id=42,
    )

    assert revoked.revoked_at is not None


def test_user_cannot_revoke_another_users_key(repository, service):
    api_key = FakeAPIKey(id=1, user_id=42)
    repository.keys[1] = api_key

    with pytest.raises(APIKeyForbiddenError):
        service.revoke_key(
            api_key_id=1,
            requesting_user_id=99,
        )

    assert api_key.revoked_at is None


def test_unknown_key_cannot_be_revoked(service):
    with pytest.raises(APIKeyNotFoundError):
        service.revoke_key(
            api_key_id=404,
            requesting_user_id=42,
        )
