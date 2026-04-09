from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trip_budget_category import TripBudgetCategoryCreate, TripBudgetCategoryRead, TripBudgetCategoryUpdate
from repositories import TripBudgetCategoryRepository
from database import get_db

router = APIRouter(prefix="/trip-budget-categories", tags=["trip-budget-categories"])

def get_trip_budget_category_repository(db: AsyncSession = Depends(get_db)) -> TripBudgetCategoryRepository:
    return TripBudgetCategoryRepository(db)

@router.get("/trips/{trip_id}", response_model=list[TripBudgetCategoryRead])
async def get_budget_categories(trip_id: int, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    return await getattr(repo, 'get_by_trip', repo.get_all)(trip_id)

@router.get("/trips/{trip_id}/{expense_type_id}", response_model=TripBudgetCategoryRead)
async def get_budget_category(trip_id: int, expense_type_id: int, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    cat = await getattr(repo, 'get_by_trip_and_expense_type', lambda x, y: None)(trip_id, expense_type_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget category not found")
    return cat

@router.put("/trips/{trip_id}/{expense_type_id}", response_model=TripBudgetCategoryRead)
async def set_budget_for_category(trip_id: int, expense_type_id: int, category: TripBudgetCategoryUpdate, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    updated = await getattr(repo, 'set_budget_for_category', repo.change)(trip_id, expense_type_id, category)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget category not found")
    return updated

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_trip_budget_category(category: TripBudgetCategoryCreate, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    return await repo.add(category)

@router.patch("/{category_id}", response_model=TripBudgetCategoryRead)
async def change_trip_budget_category(category_id: int, category: TripBudgetCategoryUpdate, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    changed = await repo.change(category_id, category)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget category not found")
    return changed

@router.delete("/{category_id}", response_model=TripBudgetCategoryRead)
async def delete_trip_budget_category(category_id: int, repo: TripBudgetCategoryRepository = Depends(get_trip_budget_category_repository)):
    deleted = await repo.delete(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget category not found")
    return deleted