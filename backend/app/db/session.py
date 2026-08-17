from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


database_url = normalize_database_url(settings.database_url)

# psycopg3 prepared statements can cause failures with Supabase/Supavisor
# transaction pooling. Disable them while keeping SQLAlchemy's normal pool,
# which is known to work with this service's existing Runsite deployment.
engine = create_engine(
    database_url,
    future=True,
    connect_args={"prepare_threshold": None} if database_url.startswith("postgresql+psycopg://") else {},
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
