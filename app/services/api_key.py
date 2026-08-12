from dataclasses import dataclass

from app.db.models.api_key import APIKey
from app.repositories.api_key import APIKeyRepository
from app.security.api_keys import (
    generate_api_key,
    get_api_key_prefix,
    hash_api_key,
)


@dataclass(frozen=True)
class CreatedAPIKey:
    api_key: APIKey
    plaintext_key: str


class APIKeyService:
    def __init__(
        self,
        repository: APIKeyRepository,
    ):
        self._repository = repository

    def create_key(
        self,
        user_id: int,
    ) -> CreatedAPIKey:
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
