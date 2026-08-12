from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.api_key import APIKeyRepository
from app.repositories.api_user import APIUserRepository
from app.schemas.api_key import APIKeyCreateResponse
from app.services.api_key import (
    APIKeyService,
    APIUserNotFoundError,
)


router = APIRouter(
    tags=["api-keys"],
)


def get_api_key_service(
    db: Session = Depends(get_db),
) -> APIKeyService:
    return APIKeyService(
        repository=APIKeyRepository(db),
        user_repository=APIUserRepository(db),
    )


@router.post(
    "/users/{user_id}/keys",
    response_model=APIKeyCreateResponse,
    status_code=201,
)
def create_api_key(
    user_id: int,
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyCreateResponse:
    try:
        result = service.create_key(user_id)
    except APIUserNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return APIKeyCreateResponse(
        id=result.api_key.id,
        user_id=result.api_key.user_id,
        key_prefix=result.api_key.key_prefix,
        key=result.plaintext_key,
        created_at=result.api_key.created_at,
    )
