from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip_member import TripMemberCreate, TripMemberRead, TripMemberUpdate
from repositories import TripMemberRepository
from database import get_db

router = APIRouter(prefix="/trip-members", tags=["trip-members"])

def get_trip_member_repository(db: AsyncSession = Depends(get_db)) -> TripMemberRepository:
    return TripMemberRepository(db)

@router.get("/", response_model=list[TripMemberRead])
async def get_trip_members(repo: TripMemberRepository = Depends(get_trip_member_repository)):
    return await repo.get_all()

@router.get("/{member_id}", response_model=TripMemberRead)
async def get_trip_member(member_id: int, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    member = await repo.get_one(member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip member not found")
    return member

@router.get("/trips/{trip_id}", response_model=list[TripMemberRead])
async def get_members_by_trip(trip_id: int, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    return await getattr(repo, 'get_by_trip', repo.get_all)(trip_id)

@router.post("/trips/{trip_id}", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_trip_member(trip_id: int, member: TripMemberCreate, repo: TripMemberRepository = Depends(get_trip_member_repository)):
    return await repo.add(member)

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