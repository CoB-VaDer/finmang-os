from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.errors import DomainError
from app.db.session import get_db
from app.models import Transaction
from app.models.enums import TransactionType
from app.schemas.common import Envelope
from app.schemas.transactions import PaginatedTransactions, TransactionCreate, TransactionOut, TransactionUpdate
from app.services.audit import record
from app.services.finance import create_transaction, validate_category

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("", response_model=Envelope[PaginatedTransactions])
def list_transactions(account_id: UUID | None = None, category_id: UUID | None = None, type: TransactionType | None = None, date_from: date | None = None, date_to: date | None = None, page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    filters = []
    if account_id: filters.append(Transaction.account_id == account_id)
    if category_id: filters.append(Transaction.category_id == category_id)
    if type: filters.append(Transaction.type == type)
    if date_from: filters.append(Transaction.transaction_date >= date_from)
    if date_to: filters.append(Transaction.transaction_date <= date_to)
    stmt = select(Transaction).where(*filters).order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    total = db.scalar(select(func.count()).select_from(Transaction).where(*filters)) or 0
    items = [TransactionOut.model_validate(x) for x in db.scalars(stmt).all()]
    return Envelope(data=PaginatedTransactions(items=items, page=page, page_size=page_size, total=total))

@router.post("", response_model=Envelope[TransactionOut], status_code=201)
def create(payload: TransactionCreate, db: Session = Depends(get_db)):
    tx = create_transaction(db, **payload.model_dump()); db.commit(); db.refresh(tx)
    return Envelope(data=TransactionOut.model_validate(tx))

@router.get("/{transaction_id}", response_model=Envelope[TransactionOut])
def get(transaction_id: UUID, db: Session = Depends(get_db)):
    tx = db.get(Transaction, transaction_id)
    if not tx: raise DomainError("TRANSACTION_NOT_FOUND", "Transaction not found.", 404)
    return Envelope(data=TransactionOut.model_validate(tx))

@router.patch("/{transaction_id}", response_model=Envelope[TransactionOut])
def update(transaction_id: UUID, payload: TransactionUpdate, db: Session = Depends(get_db)):
    tx = db.get(Transaction, transaction_id)
    if not tx: raise DomainError("TRANSACTION_NOT_FOUND", "Transaction not found.", 404)
    changes = payload.model_dump(exclude_unset=True)
    if "category_id" in changes: validate_category(db, changes["category_id"], tx.type)
    for k, v in changes.items(): setattr(tx, k, v)
    record(db, "UPDATE", "Transaction", tx.id, {k: str(v) for k, v in changes.items()}); db.commit(); db.refresh(tx)
    return Envelope(data=TransactionOut.model_validate(tx))

@router.delete("/{transaction_id}")
def delete(transaction_id: UUID, db: Session = Depends(get_db)):
    raise DomainError("METHOD_NOT_ALLOWED", "Transaction deletion is not supported in MVP.", 405)
