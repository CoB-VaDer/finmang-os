from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction


def test_model_relationships():
    assert "transactions" in Account.__mapper__.relationships
    assert "children" in Category.__mapper__.relationships
    assert "account" in Transaction.__mapper__.relationships
    assert "category" in Transaction.__mapper__.relationships
