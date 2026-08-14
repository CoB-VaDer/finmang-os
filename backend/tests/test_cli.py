from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.cli import build_parser, run
from app.models.base import Base


def test_cli_commands_registered():
    parser = build_parser()
    assert {a.dest for a in parser._actions} >= {"command"}


def test_cli_balance_workflow(capsys):
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        run(session, ["account-add", "Cash", "asset"])
        run(session, ["category-add", "Salary", "income"])
        run(session, ["category-add", "Food", "expense"])
        run(session, ["add-income", "Cash", "Salary", "100.00", "--date", str(date.today())])
        run(session, ["add-expense", "Cash", "Food", "25.50", "--date", str(date.today())])
        run(session, ["balance", "Cash"])
    assert "74.50" in capsys.readouterr().out
