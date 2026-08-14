from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.errors import DomainError
from app.db.session import get_db
from app.models import Category, Transaction
from app.models.enums import CategoryType
from app.schemas.categories import CategoryCreate, CategoryOut, CategoryUpdate
from app.schemas.common import Envelope
from app.services.audit import record

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=Envelope[list[CategoryOut]])
def list_categories(type: CategoryType | None = Query(None), db: Session = Depends(get_db)):
    stmt = select(Category).order_by(Category.name)
    if type: stmt = stmt.where(Category.type == type)
    return Envelope(data=[CategoryOut.model_validate(x) for x in db.scalars(stmt).all()])

@router.post("", response_model=Envelope[CategoryOut], status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    if payload.parent_id:
        parent = db.get(Category, payload.parent_id)
        if not parent: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
        if parent.type != payload.type: raise DomainError("CATEGORY_TYPE_MISMATCH", "Category type does not match parent category.", 422)
    c = Category(**payload.model_dump()); db.add(c); db.flush(); record(db, "CREATE", "Category", c.id, {"name": c.name}); db.commit(); db.refresh(c)
    return Envelope(data=CategoryOut.model_validate(c))

@router.get("/{category_id}", response_model=Envelope[CategoryOut])
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    c = db.get(Category, category_id)
    if not c: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
    return Envelope(data=CategoryOut.model_validate(c))

@router.patch("/{category_id}", response_model=Envelope[CategoryOut])
def update_category(category_id: UUID, payload: CategoryUpdate, db: Session = Depends(get_db)):
    c = db.get(Category, category_id)
    if not c: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
    if c.is_system: raise DomainError("SYSTEM_CATEGORY", "System categories cannot be modified or deleted.", 409)
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("parent_id"):
        if changes["parent_id"] == c.id: raise DomainError("INVALID_PARENT", "Category cannot be its own parent.", 422)
        p = db.get(Category, changes["parent_id"])
        if not p: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
        if p.type != c.type: raise DomainError("CATEGORY_TYPE_MISMATCH", "Category type does not match parent category.", 422)
    for k, v in changes.items(): setattr(c, k, v)
    record(db, "UPDATE", "Category", c.id, {k: str(v) for k, v in changes.items()}); db.commit(); db.refresh(c)
    return Envelope(data=CategoryOut.model_validate(c))

@router.delete("/{category_id}", response_model=Envelope[CategoryOut])
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    c = db.get(Category, category_id)
    if not c: raise DomainError("CATEGORY_NOT_FOUND", "Category not found.", 404)
    if c.is_system: raise DomainError("SYSTEM_CATEGORY", "System categories cannot be modified or deleted.", 409)
    used = db.scalar(select(func.count()).select_from(Transaction).where(Transaction.category_id == category_id)) or 0
    if used: raise DomainError("CATEGORY_IN_USE", "Category cannot be deleted while referenced by transactions.", 409)
    result = CategoryOut.model_validate(c); record(db, "DELETE", "Category", c.id); db.delete(c); db.commit()
    return Envelope(data=result)
