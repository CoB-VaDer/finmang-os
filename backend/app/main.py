from fastapi import FastAPI

from app.api.router import api_router
from app.api.error_handlers import register_error_handlers
from app.db.session import engine
from app.models.base import Base
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction

app = FastAPI(title="FinMang OS API", version="1.0.0")
register_error_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def ensure_database_schema():
    # Keep the API available even if the database is temporarily unreachable.
    # create_all is safe for the MVP schema and creates missing tables without
    # dropping existing data.
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"Database schema initialization skipped: {exc}", flush=True)


@app.get("/health")
def health():
    return {"status": "ok"}
