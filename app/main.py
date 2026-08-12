from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.middleware.request_logging import RequestLoggingMiddleware
from app.api.routes.api_keys import router as api_keys_router
from app.api.routes.api_users import router as api_users_router
from app.api.routes.ner import router as ner_router
from app.api.routes.sentiment import router as sentiment_router
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

app = FastAPI(
    title="PolyText API",
    description="Multilingual NLP model routing and text intelligence.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)

register_exception_handlers(app)

app.include_router(sentiment_router, prefix="/v1")
app.include_router(ner_router, prefix="/v1")
app.include_router(api_users_router, prefix="/v1")
app.include_router(api_keys_router, prefix="/v1")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "polytext",
        "version": "0.1.0",
    }