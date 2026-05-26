from datetime import datetime, timezone

from repositories import NotificationRepository, UserRepository
from schemas.notification import NotificationCreate, NotificationKind
from services.pushService import send_push


class NotificationService:
    def __init__(self, db):
        self.notification_repo = NotificationRepository(db)
        self.user_repo = UserRepository(db)

    async def create_and_send(
        self,
        user_id: int,
        trip_id: int,
        type: NotificationKind,
        message: str,
        title: str = "Trip notification",
    ) -> int:
        notification = NotificationCreate(
            trip_id=trip_id,
            user_id=user_id,
            type=type,
            message=message,
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )

        notification_id = await self.notification_repo.add(notification)

        user = await self.user_repo.get_one(user_id)

        if user and user.fcm_token:
            await send_push(
                token=user.fcm_token,
                title=title,
                body=message,
            )

        return notification_id