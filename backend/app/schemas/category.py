from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    category_type: str
    parent_id: int | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category_type: str
    parent_id: int | None
    is_system: bool
