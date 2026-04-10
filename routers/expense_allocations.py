from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.expense_allocation import ExpenseAllocationCreate, ExpenseAllocationRead, ExpenseAllocationUpdate
from repositories import ExpenseAllocationRepository
from database import get_db

router = APIRouter(prefix="/allocations", tags=["expense-allocations"])

def get_allocation_repository(db: AsyncSession = Depends(get_db)) -> ExpenseAllocationRepository:
    return ExpenseAllocationRepository(db)

@router.get("/", response_model=list[ExpenseAllocationRead])
async def get_allocations(repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    return await repo.get_all()

@router.get("/{allocation_id}", response_model=ExpenseAllocationRead)
async def get_allocation(allocation_id: int, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    alloc = await repo.get_one(allocation_id)
    if not alloc: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
    return alloc

@router.get("/expenses/{expense_id}", response_model=list[ExpenseAllocationRead])
async def get_allocations_by_expense(expense_id: int, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    return await getattr(repo, 'get_by_expense', repo.get_all)(expense_id)

@router.get("/users/{user_id}", response_model=list[ExpenseAllocationRead])
async def get_allocations_by_user(user_id: int, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    return await getattr(repo, 'get_by_user', repo.get_all)(user_id)

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_allocation(allocation: ExpenseAllocationCreate, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    return await repo.add(allocation)

@router.patch("/{allocation_id}", response_model=ExpenseAllocationRead)
async def change_allocation(allocation_id: int, allocation: ExpenseAllocationUpdate, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    changed = await repo.change(allocation_id, allocation)
    if not changed: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
    return changed

@router.delete("/{allocation_id}", response_model=ExpenseAllocationRead)
async def delete_allocation(allocation_id: int, repo: ExpenseAllocationRepository = Depends(get_allocation_repository)):
    deleted = await repo.delete(allocation_id)
    if not deleted: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
    return deleted