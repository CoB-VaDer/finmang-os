from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.errors import DomainError
from app.db.session import get_db
from app.models import Account, Transaction
from app.models.enums import TransactionType
from app.schemas.balance import BalanceOut
from app.schemas.common import Envelope
from app.services.finance import account_balance, total_balance
from sqlalchemy import func, select

router = APIRouter(tags=["Balance"])

@router.get("/accounts/{account_id}/balance", response_model=Envelope[BalanceOut])
def account_balance_endpoint(account_id: UUID, db: Session = Depends(get_db)):
    if not db.get(Account, account_id): raise DomainError("ACCOUNT_NOT_FOUND", "Account not found.", 404)
    income = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.account_id == account_id, Transaction.type == TransactionType.INCOME)) or 0
    expense = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.account_id == account_id, Transaction.type == TransactionType.EXPENSE)) or 0
    return Envelope(data=BalanceOut(total_income=income, total_expense=expense, balance=account_balance(db, account_id)))

@router.get("/balance", response_model=Envelope[BalanceOut])
def balance_endpoint(db: Session = Depends(get_db)):
    income, expense, balance = total_balance(db)
    return Envelope(data=BalanceOut(total_income=income, total_expense=expense, balance=balance))
