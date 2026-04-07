from typing import Optional

from pydantic import BaseModel, Field


class ExpenseTypeBase(BaseModel):
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None


class ExpenseTypeCreate(ExpenseTypeBase):
    pass


class ExpenseTypeRead(ExpenseTypeBase):
    id: int

    class Config:
        orm_mode = True


class ExpenseTypeUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
