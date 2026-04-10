from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeRead, ExpenseTypeUpdate
from repositories import ExpenseTypeRepository
from database import get_db

router = APIRouter(prefix="/expense-types", tags=["expense-types"])

def get_expense_type_repository(db: AsyncSession = Depends(get_db)) -> ExpenseTypeRepository:
    return ExpenseTypeRepository(db)

@router.get("/", response_model=list[ExpenseTypeRead])
async def get_expense_types(repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    return await repo.get_all()

@router.get("/{expense_type_id}", response_model=ExpenseTypeRead)
async def get_expense_type(expense_type_id: int, repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    et = await repo.get_one(expense_type_id)
    if not et:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense type not found")
    return et

@router.get("/search")
async def search_expense_types(name: Optional[str] = None, repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    return await repo.get_all()  # можно позже добавить фильтр в репозиторий

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_expense_type(expense_type: ExpenseTypeCreate, repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    return await repo.add(expense_type)

@router.patch("/{expense_type_id}", response_model=ExpenseTypeRead)
async def change_expense_type(expense_type_id: int, expense_type: ExpenseTypeUpdate, repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    changed = await repo.change(expense_type_id, expense_type)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense type not found")
    return changed

@router.delete("/{expense_type_id}", response_model=ExpenseTypeRead)
async def delete_expense_type(expense_type_id: int, repo: ExpenseTypeRepository = Depends(get_expense_type_repository)):
    deleted = await repo.delete(expense_type_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense type not found")
    return deleted