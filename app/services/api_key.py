from dataclasses import dataclass

from app.db.models.api_key import APIKey
from app.repositories.api_key import APIKeyRepository
from app.repositories.api_user import APIUserRepository
from app.security.api_keys import (
    generate_api_key,
    get_api_key_prefix,
    hash_api_key,
)


class APIUserNotFoundError(Exception):
    pass


class APIKeyNotFoundError(Exception):
    pass


class APIKeyForbiddenError(Exception):
    pass


@dataclass(frozen=True)
class CreatedAPIKey:
    api_key: APIKey
    plaintext_key: str


class APIKeyService:
    def __init__(
        self,
        repository: APIKeyRepository,
        user_repository: APIUserRepository,
    ):
        self._repository = repository
        self._user_repository = user_repository

    def create_key(self, user_id: int) -> CreatedAPIKey:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise APIUserNotFoundError(
                f"API user with id {user_id} does not exist"
            )

        plaintext_key = generate_api_key()

        api_key = self._repository.create(
            user_id=user_id,
            key_prefix=get_api_key_prefix(plaintext_key),
            key_hash=hash_api_key(plaintext_key),
        )

        return CreatedAPIKey(
            api_key=api_key,
            plaintext_key=plaintext_key,
        )

    def revoke_key(
        self,
        api_key_id: int,
        requesting_user_id: int,
    ) -> APIKey:
        api_key = self._repository.get_by_id(api_key_id)

        if api_key is None:
            raise APIKeyNotFoundError(
                f"API key with id {api_key_id} does not exist"
            )

        if api_key.user_id != requesting_user_id:
            raise APIKeyForbiddenError(
                "You cannot revoke an API key belonging to another user"
            )

        return self._repository.revoke(api_key)

    def list_keys(
        self,
        user_id: int,
    ) -> list[APIKey]:
        return self._repository.list_by_user_id(
            user_id=user_id,
        )
