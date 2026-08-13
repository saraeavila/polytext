from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_api_key
from app.db.models.api_key import APIKey
from app.db.session import get_db
from app.repositories.request_usage import (
    RequestUsageRepository,
)
from app.schemas.usage import UsageSummaryResponse
from app.services.usage import UsageService


router = APIRouter(
    prefix="/usage",
    tags=["usage"],
)


def get_usage_service(
    db: Session = Depends(get_db),
) -> UsageService:
    return UsageService(
        repository=RequestUsageRepository(db)
    )


@router.get(
    "/summary",
    response_model=UsageSummaryResponse,
)
def get_usage_summary(
    hours: int = Query(
        default=24,
        ge=1,
        le=720,
    ),
    current_key: APIKey = Depends(require_api_key),
    service: UsageService = Depends(get_usage_service),
) -> UsageSummaryResponse:
    return service.get_summary(
        api_key_id=current_key.id,
        hours=hours,
    )
