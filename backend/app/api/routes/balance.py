from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.account import BalanceOut
from app.services.balance_service import account_balance, total_balance

router = APIRouter()

@router.get("/balance")
def total(db: Session = Depends(get_db)):
    return {"data": BalanceOut(account_id=None, balance=f"{total_balance(db):.2f}")}

@router.get("/accounts/{account_id}/balance")
def account(account_id: int, db: Session = Depends(get_db)):
    return {"data": BalanceOut(account_id=account_id, balance=f"{account_balance(db, account_id):.2f}")}
