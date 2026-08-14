from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str

class Envelope(BaseModel, Generic[T]):
    data: T | None = None
    error: ErrorDetail | None = None

class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
