from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.account import AccountCreate, AccountOut
from app.services.account_service import create_account, list_accounts

router = APIRouter()

@router.get("")
def list_route(db: Session = Depends(get_db)):
    return {"data": [AccountOut.model_validate(x) for x in list_accounts(db)]}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_route(payload: AccountCreate, db: Session = Depends(get_db)):
    return {"data": AccountOut.model_validate(create_account(db, payload.name, payload.account_type))}
