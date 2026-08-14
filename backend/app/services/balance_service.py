from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.transaction import Transaction


def account_balance(db: Session, account_id: int) -> Decimal:
    txs = db.scalars(select(Transaction).where(Transaction.account_id == account_id)).all()
    return sum((t.amount if t.transaction_type == "income" else -t.amount for t in txs), Decimal("0.00"))


def total_balance(db: Session) -> Decimal:
    accounts = db.scalars(select(Account).where(Account.is_active.is_(True))).all()
    return sum((account_balance(db, a.id) for a in accounts), Decimal("0.00"))
