from fastapi import FastAPI
from app.api.routes.sentiment import router as sentiment_router

app = FastAPI(
    title="PolyText API",
    description="Multilingual NLP model routing and text intelligence.",
    version="0.1.0",
)

app.include_router(sentiment_router, prefix="/v1")
app.include_router(entity_router, prefix="/v1")
app.include_router(summarization_router, prefix="/v1")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "polytext",
        "version": "0.1.0",
    }