from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.base import Base
from app.services.account_service import create_account
from app.services.category_service import create_category
from app.services.exceptions import DomainError
from app.services.transaction_service import create_transaction


def session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return Session(engine)


def test_transaction_rules():
    with session() as db:
        account = create_account(db, "Cash", "asset")
        income = create_category(db, "Salary", "income")
        expense = create_category(db, "Food", "expense")
        tx = create_transaction(db, account.id, income.id, "income", Decimal("100.00"), date.today())
        assert tx.amount == Decimal("100.00")
        with pytest.raises(DomainError, match="CATEGORY_TYPE_MISMATCH"):
            create_transaction(db, account.id, expense.id, "income", Decimal("1"), date.today())
        with pytest.raises(DomainError, match="INVALID_AMOUNT"):
            create_transaction(db, account.id, income.id, "income", Decimal("0"), date.today())
        with pytest.raises(DomainError, match="FUTURE_TRANSACTION_DATE"):
            create_transaction(db, account.id, income.id, "income", Decimal("1"), date.today() + timedelta(days=1))
