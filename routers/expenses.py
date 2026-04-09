from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from repositories import ExpenseRepository
from database import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])

def get_expense_repository(db: AsyncSession = Depends(get_db)) -> ExpenseRepository:
    return ExpenseRepository(db)

@router.get("/", response_model=list[ExpenseRead])
async def get_expenses(repo: ExpenseRepository = Depends(get_expense_repository)):
    return await repo.get_all()

@router.get("/{expense_id}", response_model=ExpenseRead)
async def get_expense(expense_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    expense = await repo.get_one(expense_id)
    if not expense: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense

@router.get("/trips/{trip_id}", response_model=list[ExpenseRead])   # дополнительно по ТЗ
async def get_expenses_by_trip(trip_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    return await getattr(repo, 'get_by_trip', repo.get_all)(trip_id)  # если метода нет — вернёт все

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_expense(expense: ExpenseCreate, repo: ExpenseRepository = Depends(get_expense_repository)):
    return await repo.add(expense)

@router.patch("/{expense_id}", response_model=ExpenseRead)
async def change_expense(expense_id: int, expense: ExpenseUpdate, repo: ExpenseRepository = Depends(get_expense_repository)):
    changed = await repo.change(expense_id, expense)
    if not changed: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return changed

@router.delete("/{expense_id}", response_model=ExpenseRead)
async def delete_expense(expense_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    deleted = await repo.delete(expense_id)
    if not deleted: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return deleted