from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip import TripCreate, TripRead, TripUpdate
from repositories import TripRepository
from database import get_db

router = APIRouter(prefix="/trips", tags=["trips"])


def get_trip_repository(db: AsyncSession = Depends(get_db)) -> TripRepository:
    return TripRepository(db)


@router.get("/", response_model=list[TripRead])
async def get_trips(repo: TripRepository = Depends(get_trip_repository)):
    return await repo.get_all()


@router.get("/{trip_id}", response_model=TripRead)
async def get_trip(trip_id: int, repo: TripRepository = Depends(get_trip_repository)):
    trip = await repo.get_one(trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_trip(trip: TripCreate, repo: TripRepository = Depends(get_trip_repository)):
    return await repo.add(trip)


@router.patch("/{trip_id}", response_model=TripRead)
async def change_trip(trip_id: int, trip: TripUpdate, repo: TripRepository = Depends(get_trip_repository)):
    changed_trip = await repo.change(trip_id, trip)
    if not changed_trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return changed_trip


@router.delete("/{trip_id}", response_model=TripRead)
async def delete_trip(trip_id: int, repo: TripRepository = Depends(get_trip_repository)):
    deleted_trip = await repo.delete(trip_id)
    if not deleted_trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return deleted_trip
