from fastapi import FastAPI

from app.api.router import api_router
from app.api.error_handlers import register_error_handlers

app = FastAPI(title="FinMang OS API", version="1.0.0")
register_error_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
