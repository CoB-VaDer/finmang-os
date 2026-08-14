from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models.base import Base

engine = create_engine("sqlite+pysqlite:///:memory:", future=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(engine)


def override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db] = override
client = TestClient(app)


def test_accounts_categories_transactions_and_balance():
    c = client
    a = c.post("/api/v1/accounts", json={"name": "Cash", "account_type": "asset"})
    assert a.status_code == 201
    account_id = a.json()["data"]["id"]
    cat = c.post("/api/v1/categories", json={"name": "Salary", "category_type": "income"})
    assert cat.status_code == 201
    category_id = cat.json()["data"]["id"]
    tx = c.post("/api/v1/transactions", json={"account_id": account_id, "category_id": category_id, "transaction_type": "income", "amount": "100.00", "transaction_date": "2026-01-01"})
    assert tx.status_code == 201
    bal = c.get(f"/api/v1/accounts/{account_id}/balance")
    assert bal.status_code == 200
    assert bal.json()["data"]["balance"] == "100.00"


def test_transaction_delete_is_not_supported():
    assert client.delete("/api/v1/transactions/1").status_code == 405
