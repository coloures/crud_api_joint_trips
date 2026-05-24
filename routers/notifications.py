from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.notification import NotificationCreate, NotificationRead
from repositories import NotificationRepository
from database import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_repository(db: AsyncSession = Depends(get_db)) -> NotificationRepository:
    return NotificationRepository(db)


@router.get("/", response_model=list[NotificationRead])
async def get_notifications(repo: NotificationRepository = Depends(get_notification_repository)):
    return await repo.get_all()


@router.get("/users/{user_id}", response_model=list[NotificationRead])
async def get_user_notifications(user_id: int, repo: NotificationRepository = Depends(get_notification_repository)):
    return await repo.get_by_user(user_id)


@router.get("/trips/{trip_id}", response_model=list[NotificationRead])
async def get_trip_notifications(trip_id: int, repo: NotificationRepository = Depends(get_notification_repository)):
    return await repo.get_by_trip(trip_id)


@router.get("/unread", response_model=list[NotificationRead])
async def get_unread_notifications(user_id: Optional[int] = None, repo: NotificationRepository = Depends(get_notification_repository)):
    if user_id is None:
      return await repo.get_all()
    return await repo.get_unread_by_user(user_id)


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_notification(notification: NotificationCreate, repo: NotificationRepository = Depends(get_notification_repository)):
    return await repo.add(notification)


@router.patch("/{notification_id}/read", response_model=NotificationRead)
async def mark_notification_read(notification_id: int, repo: NotificationRepository = Depends(get_notification_repository)):
    updated = await repo.mark_as_read(notification_id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return updated


@router.patch("/users/{user_id}/read-all")
async def mark_all_notifications_read(user_id: int, repo: NotificationRepository = Depends(get_notification_repository)):
    await repo.mark_all_as_read(user_id)
    return {"status": "success"}


@router.delete("/{notification_id}", response_model=NotificationRead)
async def delete_notification(notification_id: int, repo: NotificationRepository = Depends(get_notification_repository)):
    deleted = await repo.delete(notification_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return deleted
