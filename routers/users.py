from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserRead, UserUpdate
from repositories import UserRepository
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@router.get("/", response_model=list[UserRead])
async def get_users(repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_all()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_one(user_id)
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/lookup")
async def lookup_user(phone: str, repo: UserRepository = Depends(get_user_repository)):
    user = await getattr(repo, 'get_by_phone', lambda x: None)(phone)
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository)):
    return await repo.add(user)

@router.patch("/{user_id}", response_model=UserRead)
async def change_user(user_id: int, user: UserUpdate, repo: UserRepository = Depends(get_user_repository)):
    changed = await repo.change(user_id, user)
    if not changed: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return changed

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    deleted = await repo.delete(user_id)
    if not deleted: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted

@router.post("/login")
async def login_user(phone_number: str, repo: UserRepository = Depends(get_user_repository)):
    user = await getattr(repo, 'get_by_phone', lambda x: None)(phone_number)
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user  # можно вернуть {"user": user, "token": "..."} позже

@router.get("/current")
async def get_current_user(user_id: int = 1, repo: UserRepository = Depends(get_user_repository)):  # временно
    user = await repo.get_one(user_id)
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user