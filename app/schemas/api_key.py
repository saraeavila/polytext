from datetime import datetime

from pydantic import BaseModel


class APIKeyCreateResponse(BaseModel):
    id: int
    user_id: int
    key_prefix: str
    key: str
    created_at: datetime
