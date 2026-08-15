from fastapi import (
    APIRouter,
    Depends,
    Response,
)
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)

from app.api.dependencies.metrics import (
    require_metrics_access,
)


router = APIRouter()


@router.get(
    "/metrics",
    include_in_schema=False,
    dependencies=[
        Depends(require_metrics_access),
    ],
)
def metrics() -> Response:
    return Response(
        content=generate_latest(),
        headers={
            "Content-Type": CONTENT_TYPE_LATEST,
        },
    )
