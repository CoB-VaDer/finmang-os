from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.errors import DomainError
from app.models import Account, Category, Transaction
from app.models.enums import TransactionType
from app.services.audit import record

MONEY = Decimal("0.01")
def money(v: Decimal) -> Decimal:
    return Decimal(v).quantize(MONEY, rounding=ROUND_HALF_UP)

def account_balance(db: Session, account_id: UUID) -> Decimal:
    income = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.account_id == account_id, Transaction.type == TransactionType.INCOME)) or Decimal("0")
    expense = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.account_id == account_id, Transaction.type == TransactionType.EXPENSE)) or Decimal("0")
    return money(Decimal(income) - Decimal(expense))

def total_balance(db: Session) -> tuple[Decimal, Decimal, Decimal]:
    income = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).join(Account).where(Account.is_active.is_(True), Transaction.type == TransactionType.INCOME)) or Decimal("0")
    expense = db.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).join(Account).where(Account.is_active.is_(True), Transaction.type == TransactionType.EXPENSE)) or Decimal("0")
    return money(Decimal(income)), money(Decimal(expense)), money(Decimal(income) - Decimal(expense))

def validate_category(db: Session, category_id: UUID, tx_type: TransactionType) -> Category:
    category = db.get(Category, category_id)
    if not category: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
    if tx_type in (TransactionType.INCOME, TransactionType.EXPENSE) and category.type.value != tx_type.value:
        raise DomainError("CATEGORY_TYPE_MISMATCH", "Category type does not match transaction type.", 422)
    return category

def create_transaction(db: Session, account_id: UUID, category_id: UUID, amount: Decimal, type: TransactionType, description: str | None, transaction_date: date) -> Transaction:
    if amount <= 0: raise DomainError("INVALID_AMOUNT", "Amount must be greater than zero.", 422)
    if transaction_date > date.today(): raise DomainError("FUTURE_DATE", "Date cannot be in the future.", 422)
    if type == TransactionType.TRANSFER: raise DomainError("TRANSFER_NOT_SUPPORTED", "Transfer transactions are not supported in MVP.", 422)
    account = db.get(Account, account_id)
    if not account: raise DomainError("ACCOUNT_NOT_FOUND", "Account not found.", 404)
    if not account.is_active: raise DomainError("ACCOUNT_INACTIVE", "Account is inactive.", 409)
    validate_category(db, category_id, type)
    tx = Transaction(account_id=account_id, category_id=category_id, amount=money(amount), type=type, description=description, transaction_date=transaction_date)
    db.add(tx); db.flush()
    record(db, "CREATE", "Transaction", tx.id, {"amount": str(tx.amount), "type": type.value})
    return tx
