from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.expense import ExpenseCreate, ExpenseUpdate
from models.expense import Expense


class ExpenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, expense_in: ExpenseCreate) -> int:
        expense_model = Expense(**expense_in.model_dump())
        self.db.add(expense_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(expense_model)
        return expense_model.id

    async def get_all(self) -> list[Expense]:
        query = select(Expense)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_one(self, expense_id: int) -> Expense | None:
        query = select(Expense).where(Expense.id == expense_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_trip(self, trip_id: int) -> list[Expense]:
        query = select(Expense).where(Expense.trip_id == trip_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_total_by_trip(self, trip_id: int) -> float | None:
        query = select(func.sum(Expense.amount)).where(Expense.trip_id == trip_id)
        result = await self.db.execute(query)
        total = result.scalar()
        return float(total) if total is not None else 0.0

    async def get_by_category(self, trip_id: int, category_id: int) -> list[Expense]:
        query = select(Expense).where(
            Expense.trip_id == trip_id,
            Expense.type_of_expense == category_id,
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def change(self, expense_id: int, updates: ExpenseUpdate) -> Expense | None:
        expense = await self.get_one(expense_id)
        if not expense:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(expense, field, value)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def delete(self, expense_id: int) -> Expense | None:
        expense = await self.db.get(Expense, expense_id)
        if not expense:
            return None
        await self.db.delete(expense)
        await self.db.commit()
        return expense
