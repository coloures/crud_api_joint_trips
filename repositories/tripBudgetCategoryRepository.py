from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip_budget_category import TripBudgetCategoryCreate, TripBudgetCategoryUpdate
from models.tripBudgetCategory import TripBudgetCategory


class TripBudgetCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, category_in: TripBudgetCategoryCreate) -> int:
        category_model = TripBudgetCategory(**category_in.model_dump())
        self.db.add(category_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(category_model)
        return category_model.id

    async def get_all(self) -> list[TripBudgetCategory]:
        result = await self.db.execute(select(TripBudgetCategory))
        return result.scalars().all()

    async def get_by_trip(self, trip_id: int) -> list[TripBudgetCategory]:
        result = await self.db.execute(
            select(TripBudgetCategory).where(TripBudgetCategory.trip_id == trip_id)
        )
        return result.scalars().all()

    async def get_category(self, trip_id: int, expense_type_id: int) -> TripBudgetCategory | None:
        result = await self.db.execute(
            select(TripBudgetCategory).where(
                TripBudgetCategory.trip_id == trip_id,
                TripBudgetCategory.expense_type_id == expense_type_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_planned_total(self, trip_id: int) -> float:
        query = select(func.sum(TripBudgetCategory.planned_amount)).where(
            TripBudgetCategory.trip_id == trip_id
        )
        result = await self.db.execute(query)
        total = result.scalar()
        return float(total) if total is not None else 0.0

    async def change(self, category_id: int, updates: TripBudgetCategoryUpdate) -> TripBudgetCategory | None:
        category = await self.db.get(TripBudgetCategory, category_id)
        if not category:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int) -> TripBudgetCategory | None:
        category = await self.db.get(TripBudgetCategory, category_id)
        if not category:
            return None
        await self.db.delete(category)
        await self.db.commit()
        return category
