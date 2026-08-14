import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.db.session import Base, get_db
from app.main import app
from app.models import Account, Category

engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base.metadata.create_all(engine)

def override_db():
    db = TestingSessionLocal()
    try: yield db
    finally: db.close()

app.dependency_overrides[get_db] = override_db
client = TestClient(app)

def seed():
    db = TestingSessionLocal()
    a = Account(name="Main", type="CHECKING", currency="MYR")
    inc = Category(name="Salary", type="INCOME")
    exp = Category(name="Groceries", type="EXPENSE")
    db.add_all([a, inc, exp]); db.commit(); db.refresh(a); db.refresh(inc); db.refresh(exp); db.close()
    return a, inc, exp
