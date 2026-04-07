from typing import Optional

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    code: str = Field(..., description="ISO currency code, e.g. RUB")
    name: str = Field(..., description="Readable currency name")
    symbol: str = Field(..., description="Currency symbol")


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyRead(CurrencyBase):
    id: int

    class Config:
        orm_mode = True


class CurrencyUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
