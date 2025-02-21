from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_user, get_user_by_email
from app.schemas import UserCreate, UserResponse
from app.auth import hash_password, create_access_token

router = APIRouter()

@router.post("/register/", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрирует нового пользователя."""
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_data.email, user_data.password)
    return {"email": user.email}