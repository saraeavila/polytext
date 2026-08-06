from fastapi import FastAPI

app = FastAPI(
    title="PolyText API",
    description="Multilingual NLP model routing and text intelligence.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "polytext",
        "version": "0.1.0",
    }