from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.currency import CurrencyCreate, CurrencyRead, CurrencyUpdate
from repositories import CurrencyRepository
from database import get_db

router = APIRouter(prefix="/currencies", tags=["currencies"])

def get_currency_repository(db: AsyncSession = Depends(get_db)) -> CurrencyRepository:
    return CurrencyRepository(db)

@router.get("/", response_model=list[CurrencyRead])
async def get_currencies(
    code: Optional[str] = None, name: Optional[str] = None, symbol: Optional[str] = None,
    repo: CurrencyRepository = Depends(get_currency_repository)
):
    return await repo.get_all()  # фильтры можно добавить в репозиторий позже

@router.get("/{currency_id}", response_model=CurrencyRead)
async def get_currency(currency_id: int, repo: CurrencyRepository = Depends(get_currency_repository)):
    currency = await repo.get_one(currency_id)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currency

@router.get("/by-code/{code}", response_model=CurrencyRead)
async def get_currency_by_code(code: str, repo: CurrencyRepository = Depends(get_currency_repository)):
    currency = await getattr(repo, 'get_by_code', lambda x: None)(code)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currency

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_currency(currency: CurrencyCreate, repo: CurrencyRepository = Depends(get_currency_repository)):
    return await repo.add(currency)

@router.patch("/{currency_id}", response_model=CurrencyRead)
async def change_currency(currency_id: int, currency: CurrencyUpdate, repo: CurrencyRepository = Depends(get_currency_repository)):
    changed = await repo.change(currency_id, currency)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return changed

@router.delete("/{currency_id}", response_model=CurrencyRead)
async def delete_currency(currency_id: int, repo: CurrencyRepository = Depends(get_currency_repository)):
    deleted = await repo.delete(currency_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return deleted