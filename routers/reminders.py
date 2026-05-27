from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories import ReminderRepository
from schemas.reminder import ReminderCreate, ReminderRead

router = APIRouter(prefix="/reminders", tags=["reminders"])


def get_reminder_repository(
    db: AsyncSession = Depends(get_db),
) -> ReminderRepository:
    return ReminderRepository(db)


@router.post(
    "/",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(
    reminder: ReminderCreate,
    repo: ReminderRepository = Depends(get_reminder_repository),
):
    return await repo.add(reminder)


@router.get("/{user_id}", response_model=list[ReminderRead])
async def get_user_reminders(
    user_id: int,
    repo: ReminderRepository = Depends(get_reminder_repository),
):
    return await repo.get_by_user(user_id)


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    repo: ReminderRepository = Depends(get_reminder_repository),
):
    deleted = await repo.delete(reminder_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    return {"status": "deleted"}