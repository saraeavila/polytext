from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from app.api.dependencies.rate_limit import (
    enforce_rate_limit,
)
from app.api.dependencies.usage import (
    mark_classification_usage,
)
from app.schemas.classification import (
    ClassificationRequest,
    ClassificationResponse,
)
from app.services.classification import (
    ClassificationService,
)
from app.services.language import LanguageService


router = APIRouter(
    tags=["classification"],
)


def get_classification_service(
    request: Request,
) -> ClassificationService:
    language_service = LanguageService(
        detector=request.app.state.language_detector
    )

    return ClassificationService(
        registry=request.app.state.model_registry,
        language_service=language_service,
    )


@router.post(
    "/classify",
    response_model=ClassificationResponse,
    dependencies=[
        Depends(enforce_rate_limit),
        Depends(mark_classification_usage),
    ],
)
def classify_text(
    request: ClassificationRequest,
    service: ClassificationService = Depends(
        get_classification_service
    ),
) -> ClassificationResponse:
    return service.classify(request)
