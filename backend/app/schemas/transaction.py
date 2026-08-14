from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int
    transaction_type: str
    amount: Decimal
    transaction_date: date
    note: str | None = None


class TransactionUpdate(BaseModel):
    amount: Decimal | None = None
    transaction_date: date | None = None
    note: str | None = None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    category_id: int
    transaction_type: str
    amount: Decimal
    transaction_date: date
    note: str | None
