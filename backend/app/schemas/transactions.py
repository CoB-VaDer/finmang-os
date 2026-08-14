from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from app.models.enums import TransactionType
from app.schemas.common import ORMBase

class TransactionCreate(BaseModel):
    account_id: UUID
    category_id: UUID
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    type: TransactionType
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date
    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: Decimal) -> Decimal:
        if v <= 0: raise ValueError("Amount must be greater than zero.")
        return v
    @field_validator("transaction_date")
    @classmethod
    def not_future(cls, v: date) -> date:
        if v > date.today(): raise ValueError("Date cannot be in the future.")
        return v

class TransactionUpdate(BaseModel):
    description: str | None = Field(default=None, max_length=255)
    category_id: UUID | None = None
    is_reconciled: bool | None = None

class TransactionOut(ORMBase):
    id: UUID
    account_id: UUID
    category_id: UUID
    amount: Decimal
    type: TransactionType
    description: str | None
    transaction_date: date
    is_reconciled: bool
    created_at: datetime
    updated_at: datetime

class PaginatedTransactions(BaseModel):
    items: list[TransactionOut]
    page: int
    page_size: int
    total: int
