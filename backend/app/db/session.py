from urllib.parse import urlsplit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


database_url = normalize_database_url(settings.database_url)
parsed_url = urlsplit(database_url)
is_transaction_pooler = parsed_url.port == 6543

engine_kwargs = {"future": True}

# Supabase/Supavisor transaction pooling (port 6543) does not support
# prepared statements and should not be combined with SQLAlchemy's connection
# pool. Psycopg3 must therefore disable automatic prepared statements and use
# one short-lived connection per unit of work.
if is_transaction_pooler:
    engine_kwargs["poolclass"] = NullPool
    engine_kwargs["connect_args"] = {"prepare_threshold": None}

engine = create_engine(database_url, **engine_kwargs)
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
