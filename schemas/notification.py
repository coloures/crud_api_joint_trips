from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


NotificationKind = Literal[
    "expense_added",
    "budget_changed",
    "reminder",
    "status_changed",
    "trip_invite",
]


class NotificationBase(BaseModel):
    trip_id: int
    user_id: int
    type: NotificationKind
    message: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    id: int

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    trip_id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[NotificationKind] = None
    message: Optional[str] = None
    is_read: Optional[bool] = None
