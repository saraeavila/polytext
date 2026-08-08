from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.sentiment import router as sentiment_router
from app.models.adapters.language.fasttext_detector import (
    FastTextLanguageDetector,
)
from app.models.setup import create_model_registry

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model_registry = create_model_registry()
    app.state.language_detector = FastTextLanguageDetector()
    yield

app = FastAPI(
    title="PolyText API",
    description="Multilingual NLP model routing and text intelligence.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(sentiment_router, prefix="/v1")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "polytext",
        "version": "0.1.0",
    }