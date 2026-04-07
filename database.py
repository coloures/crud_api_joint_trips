import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    __abstract__ = True

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://trip_user:trip_password@localhost/trip_planner"
)

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()