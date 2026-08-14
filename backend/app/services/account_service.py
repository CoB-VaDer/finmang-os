from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.account import Account
from app.services.exceptions import DomainError


def create_account(db: Session, name: str, account_type: str):
    obj = Account(name=name, account_type=account_type)
    db.add(obj); db.commit(); db.refresh(obj); return obj


def list_accounts(db: Session): return list(db.scalars(select(Account).order_by(Account.id)))


def get_account(db: Session, account_id: int):
    obj = db.get(Account, account_id)
    if not obj: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found")
    return obj


def deactivate_account(db: Session, account_id: int):
    obj = get_account(db, account_id); obj.is_active = False; db.commit(); db.refresh(obj); return obj
