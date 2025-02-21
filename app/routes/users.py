from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_user, get_user_by_email, get_referral_code_by_code
from app.schemas import UserCreate, UserResponse, UserLogin, UserRegisterWithReferralResponse
from app.auth import create_access_token, verify_password
from datetime import date

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрирует нового пользователя."""
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_data.email, user_data.password)
    return {"user_id": user.id, "email": user.email}


@router.post("/login/")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Аутентификация пользователя и возврат JWT токена."""
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"user_id": user.id, "access_token": access_token, "token_type": "bearer"}


@router.post("/register-with-referral/", response_model=UserRegisterWithReferralResponse)
async def register_with_referral(user_data: UserCreate, referral_code: str, db: AsyncSession = Depends(get_db)):
    """Регистрирует нового пользователя с использованием реферального кода."""
    referral = await get_referral_code_by_code(db, referral_code)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral code not found")
    if referral.expires_at < date.today():
        raise HTTPException(
            status_code=400, detail="Referral code has expired")
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_data.email, user_data.password)
    user.referral_user_id = referral.owner_id
    await db.commit()
    await db.refresh(user)
    return {"user_id": user.id, "email": user.email, "referral_code": referral.code, "referral_user_id": referral.owner_id}
