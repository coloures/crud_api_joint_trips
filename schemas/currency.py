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
        from_attributes = True

class CurrencyUpdate(BaseModel):
    code: Optional[str] = Field(None, description="Обновлённый ISO-код")
    name: Optional[str] = Field(None, description="Обновлённое название")
    symbol: Optional[str] = Field(None, description="Обновлённый символ")
