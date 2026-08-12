from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class APIUserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class APIUserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
