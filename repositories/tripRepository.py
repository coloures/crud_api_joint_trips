from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip import TripCreate, TripUpdate
from models.trip import Trip


class TripRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, trip_in: TripCreate) -> int:
        trip_model = Trip(**trip_in.model_dump())
        self.db.add(trip_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(trip_model)
        return trip_model.id

    async def get_all(self) -> list[Trip]:
        query = select(Trip)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_one(self, trip_id: int) -> Trip | None:
        query = select(Trip).where(Trip.id == trip_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def change(self, trip_id: int, new_trip: TripUpdate) -> Trip | None:
        trip = await self.get_one(trip_id)
        if not trip:
            return None
        update_data = new_trip.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(trip, field, value)
        await self.db.commit()
        await self.db.refresh(trip)
        return trip

    async def delete(self, trip_id: int) -> Trip | None:
        db_trip = await self.db.get(Trip, trip_id)
        if not db_trip:
            return None
        await self.db.delete(db_trip)
        await self.db.commit()
        return db_trip
