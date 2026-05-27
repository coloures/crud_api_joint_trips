from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReminderBase(BaseModel):
    user_id: int
    trip_id: Optional[int] = None
    message: str
    remind_at: datetime


class ReminderCreate(ReminderBase):
    pass


class ReminderRead(ReminderBase):
    id: int
    is_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True
