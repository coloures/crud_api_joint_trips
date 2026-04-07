from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TripBase(BaseModel):
    emoji: str = Field(..., title="Emoji representing the trip")
    title: str
    country: str
    start_date: date
    end_date: date
    currency_id: int
    budget: float
    description: Optional[str] = None


class TripCreate(TripBase):
    creator_id: int


class TripUpdate(BaseModel):
    emoji: Optional[str] = None
    title: Optional[str] = None
    country: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currency_id: Optional[int] = None
    budget: Optional[float] = None
    description: Optional[str] = None


class TripRead(TripBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True
