from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import Category
from app.services.exceptions import DomainError


def create_category(db: Session, name: str, category_type: str, parent_id: int | None = None):
    parent = db.get(Category, parent_id) if parent_id else None
    if parent_id and not parent: raise DomainError("PARENT_CATEGORY_NOT_FOUND", "Parent category not found")
    obj = Category(name=name, category_type=category_type, parent_id=parent_id)
    db.add(obj); db.commit(); db.refresh(obj); return obj


def list_categories(db: Session): return list(db.scalars(select(Category).order_by(Category.name)))
