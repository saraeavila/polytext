from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.api_user import APIUserRepository
from app.schemas.api_user import APIUserCreateRequest, APIUserResponse
from app.services.api_user import (
    APIUserAlreadyExistsError,
    APIUserService,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_api_user_service(
    db: Session = Depends(get_db),
) -> APIUserService:
    repository = APIUserRepository(db=db)
    return APIUserService(repository=repository)


@router.post(
    "",
    response_model=APIUserResponse,
    status_code=201,
)
def create_api_user(
    request: APIUserCreateRequest,
    service: APIUserService = Depends(get_api_user_service),
) -> APIUserResponse:
    try:
        user = service.create_user(
            name=request.name,
            email=str(request.email),
        )
    except APIUserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return APIUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )
