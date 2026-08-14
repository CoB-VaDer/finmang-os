from datetime import date
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.services.exceptions import DomainError


def create_transaction(db: Session, account_id: int, category_id: int, transaction_type: str, amount: Decimal, transaction_date: date, note: str | None = None):
    if amount <= 0: raise DomainError("INVALID_AMOUNT", "Amount must be greater than zero")
    if transaction_date > date.today(): raise DomainError("FUTURE_TRANSACTION_DATE", "Transaction date cannot be in the future")
    account = db.get(Account, account_id)
    category = db.get(Category, category_id)
    if not account or not account.is_active: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found or inactive")
    if not category: raise DomainError("CATEGORY_NOT_FOUND", "Category not found")
    if category.category_type != transaction_type: raise DomainError("CATEGORY_TYPE_MISMATCH", "Category type does not match transaction type")
    tx = Transaction(account_id=account_id, category_id=category_id, transaction_type=transaction_type, amount=amount.quantize(Decimal("0.01")), transaction_date=transaction_date, note=note)
    db.add(tx); db.commit(); db.refresh(tx); return tx


def list_transactions(db: Session, account_id: int | None = None, limit: int = 50):
    stmt = select(Transaction).order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).limit(limit)
    if account_id: stmt = stmt.where(Transaction.account_id == account_id)
    return list(db.scalars(stmt))
