from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware,
)

from app.api.errors import register_exception_handlers
from app.api.middleware.request_logging import RequestLoggingMiddleware
from app.api.routes.api_keys import router as api_keys_router
from app.api.routes.api_users import router as api_users_router
from app.api.routes.classification import (
    router as classification_router,
)
from app.api.routes.metrics import (
    router as metrics_router,
)
from app.api.routes.ner import router as ner_router
from app.api.routes.readiness import (
    router as readiness_router,
)
from app.api.routes.sentiment import router as sentiment_router
from app.api.routes.usage import router as usage_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.models.adapters.language.fasttext_detector import (
    FastTextLanguageDetector,
)
from app.models.setup import create_model_registry

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model_registry = create_model_registry()
    app.state.language_detector = FastTextLanguageDetector()
    yield

configure_logging()

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Multilingual NLP model routing and text intelligence.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=(
        None
        if settings.is_production
        else "/docs"
    ),
    redoc_url=(
        None
        if settings.is_production
        else "/redoc"
    ),
    openapi_url=(
        None
        if settings.is_production
        else "/openapi.json"
    ),
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=(
        settings.allowed_hosts_list
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.cors_allowed_origins_list
    ),
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-PolyText-Admin-Key",
    ],
    expose_headers=[
        "X-Request-ID",
    ],
)

app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.include_router(sentiment_router, prefix="/v1")
app.include_router(ner_router, prefix="/v1")
app.include_router(api_users_router, prefix="/v1")
app.include_router(api_keys_router, prefix="/v1")
app.include_router(usage_router, prefix="/v1")
app.include_router(classification_router, prefix="/v1")
app.include_router(metrics_router)
app.include_router(readiness_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "polytext",
        "version": "0.1.0",
    }