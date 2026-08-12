from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.api_key import APIKey


class APIKeyRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        user_id: int,
        key_prefix: str,
        key_hash: str,
    ) -> APIKey:
        api_key = APIKey(
            user_id=user_id,
            key_prefix=key_prefix,
            key_hash=key_hash,
        )

        self._db.add(api_key)
        self._db.commit()
        self._db.refresh(api_key)

        return api_key

    def get_by_hash(
        self,
        key_hash: str,
    ) -> APIKey | None:
        statement = select(APIKey).where(
            APIKey.key_hash == key_hash,
            APIKey.revoked_at.is_(None),
        )

        return self._db.scalar(statement)
