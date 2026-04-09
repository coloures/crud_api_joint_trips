from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    avatar: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar: Optional[str] = None
