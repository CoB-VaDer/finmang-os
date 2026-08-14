import argparse
from datetime import date
from decimal import Decimal

from app.db.session import SessionLocal
from app.services.account_service import create_account, list_accounts
from app.services.balance_service import account_balance, total_balance
from app.services.category_service import create_category, list_categories
from app.services.transaction_service import create_transaction, list_transactions


def build_parser():
    p = argparse.ArgumentParser(prog="finmang")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("account-add"); a.add_argument("name"); a.add_argument("account_type")
    sub.add_parser("accounts")
    c = sub.add_parser("category-add"); c.add_argument("name"); c.add_argument("category_type")
    sub.add_parser("categories")
    for kind in ("income", "expense"):
        t = sub.add_parser(f"add-{kind}"); t.add_argument("account_id"); t.add_argument("category_id"); t.add_argument("amount"); t.add_argument("--date", default=str(date.today()))
    b = sub.add_parser("balance"); b.add_argument("account_id", nargs="?")
    t = sub.add_parser("transactions"); t.add_argument("--account-id", type=int); t.add_argument("--limit", type=int, default=50)
    return p


def run(db, argv):
    args = build_parser().parse_args(argv)
    if args.command == "account-add":
        obj = create_account(db, args.name, args.account_type); print(obj.id); return
    if args.command == "accounts":
        for obj in list_accounts(db): print(obj.id, obj.name, obj.account_type, obj.is_active); return
    if args.command == "category-add":
        obj = create_category(db, args.name, args.category_type); print(obj.id); return
    if args.command == "categories":
        for obj in list_categories(db): print(obj.id, obj.name, obj.category_type); return
    if args.command.startswith("add-"):
        kind = args.command[4:]
        obj = create_transaction(db, int(args.account_id), int(args.category_id), kind, Decimal(args.amount), date.fromisoformat(args.date)); print(obj.id); return
    if args.command == "balance":
        value = account_balance(db, int(args.account_id)) if args.account_id else total_balance(db); print(f"{value:.2f}"); return
    if args.command == "transactions":
        for obj in list_transactions(db, account_id=args.account_id, limit=args.limit): print(obj.id, obj.transaction_type, obj.amount, obj.transaction_date); return


def main():
    with SessionLocal() as db:
        run(db, None)


if __name__ == "__main__":
    main()
