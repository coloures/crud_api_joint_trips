from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories import (
    ExpenseRepository,
    ExpenseAllocationRepository,
    TripMemberRepository
)
from services.debtService import DebtService

router = APIRouter(prefix="/debts", tags=["debts"])


@router.get("/trips/{trip_id}")
async def get_trip_debts(trip_id: int, db: AsyncSession = Depends(get_db)):
    service = DebtService(
        ExpenseRepository(db),
        ExpenseAllocationRepository(db),
        TripMemberRepository(db)
    )

    return await service.calculate_debts(trip_id)