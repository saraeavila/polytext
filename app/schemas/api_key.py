from datetime import datetime

from pydantic import BaseModel


class APIKeyCreateResponse(BaseModel):
    id: int
    user_id: int
    key_prefix: str
    key: str
    created_at: datetime


class APIKeyRevokeResponse(BaseModel):
    id: int
    user_id: int
    key_prefix: str
    revoked_at: datetime


class APIKeyListItem(BaseModel):
    id: int
    key_prefix: str
    rate_limit_per_minute: int
    created_at: datetime
    revoked_at: datetime | None
