from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeUpdate
from models.expenseType import ExpenseType


class ExpenseTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, expense_type_in: ExpenseTypeCreate) -> int:
        expense_type_model = ExpenseType(**expense_type_in.model_dump())
        self.db.add(expense_type_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(expense_type_model)
        return expense_type_model.id

    async def get_all(self) -> list[ExpenseType]:
        result = await self.db.execute(select(ExpenseType))
        return result.scalars().all()

    async def get_one(self, type_id: int) -> ExpenseType | None:
        result = await self.db.execute(select(ExpenseType).where(ExpenseType.id == type_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> ExpenseType | None:
        result = await self.db.execute(select(ExpenseType).where(ExpenseType.name == name))
        return result.scalar_one_or_none()

    async def change(self, type_id: int, updates: ExpenseTypeUpdate) -> ExpenseType | None:
        expense_type = await self.get_one(type_id)
        if not expense_type:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(expense_type, field, value)
        await self.db.commit()
        await self.db.refresh(expense_type)
        return expense_type

    async def delete(self, type_id: int) -> ExpenseType | None:
        expense_type = await self.db.get(ExpenseType, type_id)
        if not expense_type:
            return None
        await self.db.delete(expense_type)
        await self.db.commit()
        return expense_type
