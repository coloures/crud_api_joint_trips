from typing import Optional

from pydantic import BaseModel


class TripMemberBase(BaseModel):
    trip_id: int
    member_id: int
    status: str
    role: str


class TripMemberCreate(TripMemberBase):
    pass


class TripMemberRead(TripMemberBase):
    id: int

    class Config:
        orm_mode = True


class TripMemberUpdate(BaseModel):
    trip_id: Optional[int] = None
    member_id: Optional[int] = None
    status: Optional[str] = None
    role: Optional[str] = None
