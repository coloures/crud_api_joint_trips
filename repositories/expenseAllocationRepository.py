from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.expense_allocation import (
    ExpenseAllocationCreate,
    ExpenseAllocationUpdate,
)
from models.expenseAllocation import ExpenseAllocation


class ExpenseAllocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, allocation_in: ExpenseAllocationCreate) -> int:
        allocation_model = ExpenseAllocation(**allocation_in.model_dump())
        self.db.add(allocation_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(allocation_model)
        return allocation_model.id

    async def get_all(self) -> list[ExpenseAllocation]:
        result = await self.db.execute(select(ExpenseAllocation))
        return result.scalars().all()

    async def get_by_expense(self, expense_id: int) -> list[ExpenseAllocation]:
        result = await self.db.execute(
            select(ExpenseAllocation).where(ExpenseAllocation.expense_id == expense_id)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> list[ExpenseAllocation]:
        result = await self.db.execute(
            select(ExpenseAllocation).where(ExpenseAllocation.user_id == user_id)
        )
        return result.scalars().all()

    async def change(self, allocation_id: int, updates: ExpenseAllocationUpdate) -> ExpenseAllocation | None:
        allocation = await self.db.get(ExpenseAllocation, allocation_id)
        if not allocation:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(allocation, field, value)
        await self.db.commit()
        await self.db.refresh(allocation)
        return allocation

    async def delete(self, allocation_id: int) -> ExpenseAllocation | None:
        allocation = await self.db.get(ExpenseAllocation, allocation_id)
        if not allocation:
            return None
        await self.db.delete(allocation)
        await self.db.commit()
        return allocation
