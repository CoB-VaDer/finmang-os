from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.errors import DomainError
from app.api.accounts import router as accounts_router
from app.api.categories import router as categories_router
from app.api.transactions import router as transactions_router
from app.api.balance import router as balance_router

app = FastAPI(title=settings.app_name, version=settings.app_version, description="Personal Financial Operating System API")

@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content={"data": None, "error": {"code": exc.code, "message": exc.message}})

@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(_: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = errors[0].get("msg", "Invalid request.") if errors else "Malformed request body."
    code = "VALIDATION_ERROR"
    if errors:
        loc = errors[0].get("loc", ())
        if "amount" in loc: code, message = "INVALID_AMOUNT", "Amount must be greater than zero."
        elif "transaction_date" in loc: code, message = "FUTURE_DATE", "Date cannot be in the future."
    return JSONResponse(status_code=422, content={"data": None, "error": {"code": code, "message": message}})

@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}

app.include_router(accounts_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")
app.include_router(balance_router, prefix="/api/v1")
