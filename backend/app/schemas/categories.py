from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from app.models.enums import CategoryType
from app.schemas.common import ORMBase

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: CategoryType
    parent_id: UUID | None = None
    color: str | None = Field(default=None, min_length=7, max_length=7)
    @field_validator("color")
    @classmethod
    def hex_color(cls, v: str | None) -> str | None:
        if v is not None and (not v.startswith("#") or len(v) != 7 or any(c not in "0123456789abcdefABCDEF" for c in v[1:])): raise ValueError("Color must be a valid hex color.")
        return v.upper() if v else v

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, min_length=7, max_length=7)
    parent_id: UUID | None = None

class CategoryOut(ORMBase):
    id: UUID
    name: str
    type: CategoryType
    parent_id: UUID | None
    color: str | None
    is_system: bool
    created_at: datetime
