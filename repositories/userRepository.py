from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserUpdate 
from models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, user_in: UserCreate) -> int:
        user_model = User(**user_in.model_dump())
        self.db.add(user_model)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(user_model)
        return user_model.id

    async def get_all(self) -> list[User]:
        query = select(User)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_one(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def change(self, user_id: int, new_user: UserUpdate) -> User | None:
        user = await self.get_one(user_id)
        if not user:
            return None
        update_data = new_user.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> User | None:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            return None
        await self.db.delete(db_user)
        await self.db.commit()
        return db_user
