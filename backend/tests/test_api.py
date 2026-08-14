from datetime import date, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.main import app
from app.schemas.transactions import TransactionCreate
from app.models.enums import TransactionType


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_transaction_amount_must_be_positive():
    with pytest.raises(ValidationError):
        TransactionCreate(
            account_id="00000000-0000-0000-0000-000000000001",
            category_id="00000000-0000-0000-0000-000000000002",
            amount=Decimal("0.00"),
            type=TransactionType.EXPENSE,
            transaction_date=date.today(),
        )


def test_transaction_date_cannot_be_future():
    with pytest.raises(ValidationError):
        TransactionCreate(
            account_id="00000000-0000-0000-0000-000000000001",
            category_id="00000000-0000-0000-0000-000000000002",
            amount=Decimal("10.00"),
            type=TransactionType.EXPENSE,
            transaction_date=date.today() + timedelta(days=1),
        )
