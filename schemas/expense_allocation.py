from typing import Optional

from pydantic import BaseModel, Field


class ExpenseAllocationBase(BaseModel):
    expense_id: int
    user_id: int
    amount: float = Field(..., gt=0)
    is_paid: Optional[bool] = Field(default=False)


class ExpenseAllocationCreate(ExpenseAllocationBase):
    pass


class ExpenseAllocationRead(ExpenseAllocationBase):
    id: int

    class Config:
        orm_mode = True


class ExpenseAllocationUpdate(BaseModel):
    expense_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0)
    is_paid: Optional[bool] = None
