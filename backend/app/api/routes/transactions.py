from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.services.transaction_service import create_transaction, list_transactions

router = APIRouter()

@router.get("")
def list_route(account_id: int | None = None, limit: int = 50, db: Session = Depends(get_db)):
    return {"data": [TransactionOut.model_validate(x) for x in list_transactions(db, account_id, limit)]}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_route(payload: TransactionCreate, db: Session = Depends(get_db)):
    obj = create_transaction(db, **payload.model_dump())
    return {"data": TransactionOut.model_validate(obj)}

@router.delete("/{transaction_id}")
def delete_route(transaction_id: int):
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Transaction deletion is not supported")
