from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import repositories
from datetime import date
from database import get_db

router = APIRouter(prefix="/trips", tags=["trips"])

def get_trip_repository(db: Session = Depends(get_db)):
    return repositories.tripRepository(db)


@router.get("/", response_model=list[schemas.trip.TripResponse])
async def get_trips(repo: repositories.tripRepository = Depends(get_trip_repository)):
    trips = await repo.get_all()
    return trips

@router.get("/{id}")
async def get_trip(id: int, repo: repositories.tripRepository = Depends(get_trip_repository)):
    trip = await repo.get_one(id)
    return trip

@router.post("/", response_model=int)
async def add_trip(trip: schemas.trip.Trip, repo: repositories.tripRepository = Depends(get_trip_repository)):
    trip_id = await repo.add(trip)
    return trip_id

@router.patch("/{id}", response_model=schemas.trip.TripResponse)
async def change_trip(id: int, trip: schemas.trip.TripChange, repo: repositories.tripRepository = Depends(get_trip_repository)):
    changed_trip = await repo.change(id, trip)
    return changed_trip

@router.delete("/{id}", response_model=schemas.trip.TripResponse)
async def delete_trip(id: int, repo: repositories.tripRepository = Depends(get_trip_repository)):
    deleted_trip = await repo.delete(id)
    return deleted_trip