from typing import Optional

from pydantic import BaseModel, Field


class TripBudgetCategoryBase(BaseModel):
    trip_id: int
    expense_type_id: int
    planned_amount: float = Field(..., ge=0)


class TripBudgetCategoryCreate(TripBudgetCategoryBase):
    pass


class TripBudgetCategoryRead(TripBudgetCategoryBase):
    id: int

    class Config:
        orm_mode = True


class TripBudgetCategoryUpdate(BaseModel):
    trip_id: Optional[int] = None
    expense_type_id: Optional[int] = None
    planned_amount: Optional[float] = Field(None, ge=0)
