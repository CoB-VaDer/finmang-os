from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.services.exceptions import DomainError


def register_error_handlers(app: FastAPI):
    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"error": {"code": exc.code, "message": exc.message}})
