from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.currency import CurrencyCreate, CurrencyUpdate
from models.currency import Currency


class CurrencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, currency_in: CurrencyCreate) -> int:
        currency_model = Currency(**currency_in.model_dump())
        self.db.add(currency_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(currency_model)
        return currency_model.id

    async def get_all(self) -> list[Currency]:
        query = select(Currency)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_one(self, currency_id: int) -> Currency | None:
        query = select(Currency).where(Currency.id == currency_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Currency | None:
        query = select(Currency).where(Currency.code == code)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def change(self, currency_id: int, currency_update: CurrencyUpdate) -> Currency | None:
        currency = await self.get_one(currency_id)
        if not currency:
            return None
        update_data = currency_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(currency, field, value)
        await self.db.commit()
        await self.db.refresh(currency)
        return currency

    async def delete(self, currency_id: int) -> Currency | None:
        currency = await self.db.get(Currency, currency_id)
        if not currency:
            return None
        await self.db.delete(currency)
        await self.db.commit()
        return currency
