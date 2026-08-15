from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.admin import (
    require_admin_key,
)
from app.api.dependencies.auth import require_api_key
from app.db.models.api_key import APIKey
from app.db.session import get_db
from app.repositories.api_key import APIKeyRepository
from app.repositories.api_user import APIUserRepository
from app.schemas.api_key import (
    APIKeyCreateResponse,
    APIKeyListItem,
    APIKeyRevokeResponse,
)
from app.services.api_key import (
    APIKeyForbiddenError,
    APIKeyNotFoundError,
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
    dependencies=[
        Depends(require_admin_key),
    ],
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


@router.post(
    "/keys/{api_key_id}/revoke",
    response_model=APIKeyRevokeResponse,
)
def revoke_api_key(
    api_key_id: int,
    current_key: APIKey = Depends(require_api_key),
    service: APIKeyService = Depends(get_api_key_service),
) -> APIKeyRevokeResponse:
    try:
        revoked = service.revoke_key(
            api_key_id=api_key_id,
            requesting_user_id=current_key.user_id,
        )

    except APIKeyNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except APIKeyForbiddenError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc

    return APIKeyRevokeResponse(
        id=revoked.id,
        user_id=revoked.user_id,
        key_prefix=revoked.key_prefix,
        revoked_at=revoked.revoked_at,
    )


@router.get(
    "/keys",
    response_model=list[APIKeyListItem],
)
def list_api_keys(
    current_key: APIKey = Depends(require_api_key),
    service: APIKeyService = Depends(get_api_key_service),
) -> list[APIKeyListItem]:
    api_keys = service.list_keys(
        user_id=current_key.user_id,
    )

    return [
        APIKeyListItem(
            id=api_key.id,
            key_prefix=api_key.key_prefix,
            rate_limit_per_minute=api_key.rate_limit_per_minute,
            created_at=api_key.created_at,
            revoked_at=api_key.revoked_at,
        )
        for api_key in api_keys
    ]
