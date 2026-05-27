from repositories import TripMemberRepository, TripRepository
from services.notificationService import NotificationService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.trip_member import TripMemberCreate, TripMemberRead, TripMemberUpdate

router = APIRouter(prefix="/trip-members", tags=["trip-members"])


def get_trip_member_repository(db: AsyncSession = Depends(get_db)) -> TripMemberRepository:
    return TripMemberRepository(db)


@router.get("/", response_model=list[TripMemberRead])
async def get_trip_members(repo: TripMemberRepository = Depends(get_trip_member_repository)):
    return await repo.get_all()


@router.get("/trips/{trip_id}", response_model=list[TripMemberRead])
async def get_members_by_trip(trip_id: int, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    return await repo.get_by_trip(trip_id)


@router.get("/{member_id}", response_model=TripMemberRead)
async def get_trip_member(member_id: int, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    member = await repo.get_one(member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip member not found")
    return member


@router.post("/trips/{trip_id}", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_trip_member(
    trip_id: int,
    member: TripMemberCreate,
    db: AsyncSession = Depends(get_db),
):
    member_repo = TripMemberRepository(db)
    trip_repo = TripRepository(db)
    notification_service = NotificationService(db)

    member_id = await member_repo.add(member)

    trip = await trip_repo.get_one(trip_id)

    await notification_service.create_and_send(
        user_id=member.member_id,
        trip_id=trip_id,
        type="trip_invite",
        title="Trip invitation",
        message=f"You were invited to trip: {trip.title if trip else 'Unknown trip'}",
    )

    return member_id


@router.patch("/{member_id}", response_model=TripMemberRead)
async def change_trip_member(member_id: int, member: TripMemberUpdate, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    changed = await repo.change(member_id, member)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip member not found")
    return changed


@router.delete("/{member_id}", response_model=TripMemberRead)
async def delete_trip_member(member_id: int, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    deleted = await repo.delete(member_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip member not found")
    return deleted
