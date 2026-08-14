from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    name: str
    account_type: str


class AccountUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    account_type: str
    is_active: bool


class BalanceOut(BaseModel):
    account_id: int | None
    balance: str
