from datetime import datetime, timezone

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

    def get_by_id(self, api_key_id: int) -> APIKey | None:
        return self._db.get(APIKey, api_key_id)

    def revoke(self, api_key: APIKey) -> APIKey:
        if api_key.revoked_at is None:
            api_key.revoked_at = datetime.now(timezone.utc)

            self._db.commit()
            self._db.refresh(api_key)

        return api_key

    def list_by_user_id(
        self,
        user_id: int,
    ) -> list[APIKey]:
        statement = (
            select(APIKey)
            .where(APIKey.user_id == user_id)
            .order_by(APIKey.created_at.desc())
        )

        return list(
            self._db.scalars(statement).all()
        )
