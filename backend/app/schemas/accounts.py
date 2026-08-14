from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from app.models.enums import AccountType
from app.schemas.common import ORMBase

class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: AccountType
    currency: str = Field(min_length=3, max_length=3)
    institution: str | None = Field(default=None, max_length=100)
    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: str) -> str: return v.upper()

class AccountUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    institution: str | None = Field(default=None, max_length=100)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: str | None) -> str | None: return v.upper() if v else v

class AccountOut(ORMBase):
    id: UUID
    name: str
    type: AccountType
    balance: Decimal
    currency: str
    institution: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
