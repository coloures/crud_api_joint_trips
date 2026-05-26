from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.reminder import Reminder
from schemas.reminder import ReminderCreate


class ReminderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, reminder_in: ReminderCreate) -> int:
        reminder = Reminder(**reminder_in.model_dump())
        self.db.add(reminder)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(reminder)
        return reminder.id

    async def get_due_unsent(self, now: datetime) -> list[Reminder]:
        result = await self.db.execute(
            select(Reminder).where(
                Reminder.remind_at <= now,
                Reminder.is_sent == False,
            )
        )
        return result.scalars().all()

    async def mark_sent(self, reminder_id: int) -> None:
        reminder = await self.db.get(Reminder, reminder_id)
        if reminder:
            reminder.is_sent = True
            await self.db.commit()
    
    async def get_by_user(self, user_id: int) -> list[Reminder]:
        result = await self.db.execute(
            select(Reminder).where(
                Reminder.user_id == user_id
            )
        )
        return result.scalars().all()
    
    async def delete(self, reminder_id: int) -> Reminder | None:
        reminder = await self.db.get(Reminder, reminder_id)
        if not reminder:
            return None
        await self.db.delete(reminder)
        await self.db.commit()
        return reminder