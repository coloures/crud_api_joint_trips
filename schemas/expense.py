from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    trip_id: int
    user_id_pay: int
    amount: float = Field(..., gt=0)
    date: date
    type_of_expense: int
    currency_id: int
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int

    class Config:
        orm_mode = True


class ExpenseUpdate(BaseModel):
    trip_id: Optional[int] = None
    user_id_pay: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None
    type_of_expense: Optional[int] = None
    currency_id: Optional[int] = None
    description: Optional[str] = None
