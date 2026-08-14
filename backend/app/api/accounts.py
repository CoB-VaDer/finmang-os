from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.errors import DomainError
from app.db.session import get_db
from app.models import Account
from app.schemas.accounts import AccountCreate, AccountOut, AccountUpdate
from app.schemas.common import Envelope
from app.services.audit import record
from app.services.finance import account_balance

router = APIRouter(prefix="/accounts", tags=["Accounts"])

def out(db: Session, a: Account) -> AccountOut:
    data = AccountOut.model_validate(a)
    data.balance = account_balance(db, a.id)
    return data

@router.get("", response_model=Envelope[list[AccountOut]])
def list_accounts(include_inactive: bool = Query(False), db: Session = Depends(get_db)):
    stmt = select(Account)
    if not include_inactive: stmt = stmt.where(Account.is_active.is_(True))
    return Envelope(data=[out(db, a) for a in db.scalars(stmt.order_by(Account.created_at)).all()])

@router.post("", response_model=Envelope[AccountOut], status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    a = Account(**payload.model_dump()); db.add(a); db.flush(); record(db, "CREATE", "Account", a.id, {"name": a.name}); db.commit(); db.refresh(a)
    return Envelope(data=out(db, a))

@router.get("/{account_id}", response_model=Envelope[AccountOut])
def get_account(account_id: UUID, db: Session = Depends(get_db)):
    a = db.get(Account, account_id)
    if not a: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found.", 404)
    return Envelope(data=out(db, a))

@router.patch("/{account_id}", response_model=Envelope[AccountOut])
def update_account(account_id: UUID, payload: AccountUpdate, db: Session = Depends(get_db)):
    a = db.get(Account, account_id)
    if not a: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found.", 404)
    if not a.is_active: raise DomainError("ACCOUNT_INACTIVE", "Account is inactive.", 409)
    changes = payload.model_dump(exclude_unset=True)
    for k, v in changes.items(): setattr(a, k, v)
    record(db, "UPDATE", "Account", a.id, {k: str(v) for k, v in changes.items()}); db.commit(); db.refresh(a)
    return Envelope(data=out(db, a))

@router.delete("/{account_id}", response_model=Envelope[AccountOut])
def delete_account(account_id: UUID, db: Session = Depends(get_db)):
    a = db.get(Account, account_id)
    if not a: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found.", 404)
    a.is_active = False
    record(db, "SOFT_DELETE", "Account", a.id); db.commit(); db.refresh(a)
    return Envelope(data=out(db, a))
