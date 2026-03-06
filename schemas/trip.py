from pydantic import BaseModel
from datetime import date
from typing import Optional

class Trip(BaseModel):
    name: str
    description: Optional[str] = None
    destination: str
    start_date: date
    end_date: date
    total_budget: float

class TripChange(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_budget: Optional[float] = None

class TripResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    destination: str
    start_date: date
    end_date: date
    total_budget: float
