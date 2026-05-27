from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories import ExpenseRepository, TripMemberRepository
from services.notificationService import NotificationService
from schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_expense_repository(db: AsyncSession = Depends(get_db)) -> ExpenseRepository:
    return ExpenseRepository(db)


@router.get("/", response_model=list[ExpenseRead])
async def get_expenses(repo: ExpenseRepository = Depends(get_expense_repository)):
    return await repo.get_all()


@router.get("/trips/{trip_id}", response_model=list[ExpenseRead])
async def get_expenses_by_trip(trip_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    return await repo.get_by_trip(trip_id)


@router.get("/{expense_id}", response_model=ExpenseRead)
async def get_expense(expense_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    expense = await repo.get_one(expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_expense(
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
):
    expense_repo = ExpenseRepository(db)
    member_repo = TripMemberRepository(db)
    notification_service = NotificationService(db)

    expense_id = await expense_repo.add(expense)

    members = await member_repo.get_by_trip(expense.trip_id)
    recipient_ids = [m.member_id for m in members if m.member_id != expense.user_id_pay]

    for user_id in recipient_ids:
        await notification_service.create_and_send(
            user_id=user_id,
            trip_id=expense.trip_id,
            type="expense_added",
            title="New expense",
            message=f"New expense was added: {expense.amount}",
        )

    return expense_id

@router.patch("/{expense_id}", response_model=ExpenseRead)
async def change_expense(expense_id: int, expense: ExpenseUpdate, repo: ExpenseRepository = Depends(get_expense_repository)):
    changed = await repo.change(expense_id, expense)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return changed


@router.delete("/{expense_id}", response_model=ExpenseRead)
async def delete_expense(expense_id: int, repo: ExpenseRepository = Depends(get_expense_repository)):
    deleted = await repo.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return deleted
