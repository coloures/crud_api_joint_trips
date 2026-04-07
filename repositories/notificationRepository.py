from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.notification import NotificationCreate, NotificationUpdate
from models.notification import Notification


class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, notification_in: NotificationCreate) -> int:
        notification_model = Notification(**notification_in.model_dump())
        self.db.add(notification_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(notification_model)
        return notification_model.id

    async def get_all(self) -> list[Notification]:
        result = await self.db.execute(select(Notification))
        return result.scalars().all()

    async def get_by_user(self, user_id: int) -> list[Notification]:
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_trip(self, trip_id: int) -> list[Notification]:
        result = await self.db.execute(
            select(Notification).where(Notification.trip_id == trip_id)
        )
        return result.scalars().all()

    async def get_unread_by_user(self, user_id: int) -> list[Notification]:
        result = await self.db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,  # noqa: E712
            )
        )
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int) -> Notification | None:
        notification = await self.db.get(Notification, notification_id)
        if not notification:
            return None
        notification.is_read = True
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def mark_all_as_read(self, user_id: int) -> int:
        notifications = await self.get_unread_by_user(user_id)
        for notification in notifications:
            notification.is_read = True
        await self.db.commit()
        return len(notifications)

    async def change(self, notification_id: int, updates: NotificationUpdate) -> Notification | None:
        notification = await self.db.get(Notification, notification_id)
        if not notification:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(notification, field, value)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def delete(self, notification_id: int) -> Notification | None:
        notification = await self.db.get(Notification, notification_id)
        if not notification:
            return None
        await self.db.delete(notification)
        await self.db.commit()
        return notification
