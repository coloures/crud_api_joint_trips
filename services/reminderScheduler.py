from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import SessionLocal
from repositories import ReminderRepository
from services.notificationService import NotificationService

scheduler = AsyncIOScheduler()


async def check_reminders():
    async with SessionLocal() as db:
        reminder_repo = ReminderRepository(db)
        notification_service = NotificationService(db)

        now = datetime.now(timezone.utc)
        reminders = await reminder_repo.get_due_unsent(now)

        for reminder in reminders:
            await notification_service.create_and_send(
                user_id=reminder.user_id,
                trip_id=reminder.trip_id,
                type="reminder",
                title="Reminder",
                message=reminder.message,
            )

            await reminder_repo.mark_sent(reminder.id)


def start_reminder_scheduler():
    scheduler.add_job(check_reminders, "interval", seconds=30)
    scheduler.start()


def stop_reminder_scheduler():
    scheduler.shutdown()