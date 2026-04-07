from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip_member import TripMemberCreate, TripMemberUpdate
from models.tripMember import TripMember


class TripMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, member_in: TripMemberCreate) -> int:
        member_model = TripMember(**member_in.model_dump())
        self.db.add(member_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(member_model)
        return member_model.id

    async def get_all(self) -> list[TripMember]:
        result = await self.db.execute(select(TripMember))
        return result.scalars().all()

    async def get_by_trip(self, trip_id: int) -> list[TripMember]:
        result = await self.db.execute(
            select(TripMember).where(TripMember.trip_id == trip_id)
        )
        return result.scalars().all()

    async def get_by_member(self, member_id: int) -> list[TripMember]:
        result = await self.db.execute(
            select(TripMember).where(TripMember.member_id == member_id)
        )
        return result.scalars().all()

    async def get_one(self, member_id: int) -> TripMember | None:
        return await self.db.get(TripMember, member_id)

    async def change(self, member_id: int, updates: TripMemberUpdate) -> TripMember | None:
        member = await self.get_one(member_id)
        if not member:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(member, field, value)
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def delete(self, member_id: int) -> TripMember | None:
        member = await self.db.get(TripMember, member_id)
        if not member:
            return None
        await self.db.delete(member)
        await self.db.commit()
        return member
