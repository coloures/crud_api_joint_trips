from sqlalchemy.orm import Session
from sqlalchemy import select
import schemas
import models

class tripRepository:

    def __init__(self, db: Session):
        self.db = db

    async def add(self, trip: schemas.Trip):
        trip = models.Trip(**trip.model_dump())
        self.db.add(trip)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(trip)
        return trip.id

    async def get_all(self):
        query = select(models.Trip)
        result = await self.db.execute(query)
        trip_models = result.scalars().all()
        return trip_models
    
    async def get_one(self, trip_id: int):
        query = select(models.Trip).where(models.Trip.id == trip_id)
        result = await self.db.execute(query)
        trip_model = result.scalar()
        return trip_model
    
    async def change(self, trip_id: int, new_trip: schemas.TripChange):
        trip = await self.get_one(trip_id)

        if not trip:
            return None
        
        update_data = new_trip.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(trip, field, value)

        await self.db.commit()
        await self.db.refresh(trip)

        return trip
    
    async def delete(self, trip_id: int):

        db_trip = await self.db.get(models.Trip, trip_id)

        if not db_trip:
            return None

        await self.db.delete(db_trip)
        await self.db.commit()

        return db_trip