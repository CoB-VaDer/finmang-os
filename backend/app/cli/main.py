import argparse
from datetime import date
from decimal import Decimal
from app.db.session import SessionLocal
from app.models import Account, Category
from app.models.enums import CategoryType, TransactionType
from app.services.finance import create_transaction, total_balance
from sqlalchemy import select

def choose_category(db, kind):
    categories = db.scalars(select(Category).where(Category.type == kind).order_by(Category.name)).all()
    if not categories: raise SystemExit(f"No {kind.value} categories exist. Create one through the API first.")
    for i, c in enumerate(categories, 1): print(f"{i}. {c.name}")
    return categories[int(input("Category #: ")) - 1].id

def add(kind):
    with SessionLocal() as db:
        accounts = db.scalars(select(Account).where(Account.is_active.is_(True)).order_by(Account.name)).all()
        if not accounts: raise SystemExit("No active accounts exist. Create one through the API first.")
        for i, a in enumerate(accounts, 1): print(f"{i}. {a.name} ({a.currency})")
        account = accounts[int(input("Account #: ")) - 1]
        amount = Decimal(input("Amount: "))
        category_id = choose_category(db, kind)
        description = input("Description (optional): ").strip() or None
        tx_type = TransactionType.INCOME if kind == CategoryType.INCOME else TransactionType.EXPENSE
        tx = create_transaction(db, account.id, category_id, amount, tx_type, description, date.today())
        db.commit(); print(f"Transaction added: {tx.id}")

def main():
    p = argparse.ArgumentParser(prog="finmang")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("add-income"); sub.add_parser("add-expense"); sub.add_parser("balance")
    args = p.parse_args()
    if args.command == "add-income": add(CategoryType.INCOME)
    elif args.command == "add-expense": add(CategoryType.EXPENSE)
    else:
        with SessionLocal() as db:
            income, expense, balance = total_balance(db)
            print(f"Income: {income:.2f}\nExpense: {expense:.2f}\nBalance: {balance:.2f}")

if __name__ == "__main__": main()
