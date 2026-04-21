from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import UserRepository
from schemas.user import UserUpdate
import httpx
import os
from database import get_db

router = APIRouter(prefix="/avatars", tags=["avatars"])

def get_avatar_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
IMGBB_UPLOAD_URL = os.getenv("IMGBB_UPLOAD_URL")


@router.post("/upload/{user_id}")
async def upload_to_imgbb(user_id: int, file: UploadFile = File(...), repo: UserRepository = Depends(get_avatar_repository)):
    if not IMGBB_API_KEY:
        raise HTTPException(status_code=500, detail="IMGBB_API_KEY not set")
    
    user = await repo.get_one(user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    try:
        content = await file.read()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                IMGBB_UPLOAD_URL,
                params={"key": IMGBB_API_KEY},
                files={
                    "image": (
                        file.filename or "upload.jpg",
                        content,
                        file.content_type,
                    )
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "imgBB вернул ошибку",
                    "status_code": response.status_code,
                    "body": response.text,
                },
            )

        payload = response.json()

        if not payload.get("success"):
            raise HTTPException(status_code=502, detail=payload)
        
        image_url = payload["data"]["display_url"]

        updated_user = await repo.change(
            user_id=user_id,
            new_user=UserUpdate(avatar=image_url)
        )

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка сети: {str(e)}")
    finally:
        await file.close()