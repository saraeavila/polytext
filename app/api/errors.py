from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.errors import ModelOutputError
from app.models.registry import UnsupportedModelError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnsupportedModelError)
    async def unsupported_model_handler(
        request: Request,
        exc: UnsupportedModelError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "unsupported_model",
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(ModelOutputError)
    async def model_output_handler(
        request: Request,
        exc: ModelOutputError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "model_output_error",
                    "message": "The model returned an unexpected result.",
                }
            },
        )
