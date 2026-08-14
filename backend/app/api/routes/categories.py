from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.category_service import create_category, list_categories

router = APIRouter()

@router.get("", response_model=dict)
def list_route(db: Session = Depends(get_db)):
    return {"data": [CategoryOut.model_validate(x) for x in list_categories(db)]}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_route(payload: CategoryCreate, db: Session = Depends(get_db)):
    return {"data": CategoryOut.model_validate(create_category(db, payload.name, payload.category_type, payload.parent_id))}
