from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.crud import (
    create_referral_code,
    get_referral_code_by_email,
    get_referral_code_by_user_id,
    get_referral_code_by_code,
    delete_referral_code
)
from app.schemas import ReferralCreate, ReferralResponse, ReferralUserResponse
from app.redis_cache import delete_referral_code_from_cache, get_referral_code_from_cache, set_referral_code_in_cache
from app.models import User

router = APIRouter()


@router.post("/referral/create/", response_model=ReferralResponse)
async def create_referral(user_id: int, referral_data: ReferralCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый реферальный код для пользователя."""
    referral = await create_referral_code(db, user_id, referral_data.code, referral_data.expires_at)
    if not referral:
        raise HTTPException(
            status_code=400, detail="User already has an active referral code")
    await set_referral_code_in_cache(f"user:{user_id}:referral", referral.code)
    return {"user_id": user_id, "code": referral.code, "expires_at": referral.expires_at}


@router.get("/referral/{email}", response_model=ReferralResponse)
async def get_referral_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """Возвращает реферальный код по email пользователя."""
    cached_code = await get_referral_code_from_cache(f"email:{email}:referral")
    if cached_code:
        referral_code = cached_code.decode('utf-8')
        referral = await get_referral_code_by_code(db, referral_code)
        if referral:
            return {"user_id": referral.owner_id, "code": referral_code, "expires_at": referral.expires_at}
        else:
            raise HTTPException(
                status_code=404, detail="Referral code not found in database")
    referral = await get_referral_code_by_email(db, email)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral code not found")
    await set_referral_code_in_cache(f"email:{email}:referral", referral.code)
    return {"user_id": referral.owner_id, "code": referral.code, "expires_at": referral.expires_at}


@router.get("/referrals/{user_id}", response_model=list[ReferralUserResponse])
async def get_referrals(user_id: int, db: AsyncSession = Depends(get_db)):
    """Возвращает список пользователей, зарегистрированных по реферальному коду пользователя."""
    result = await db.execute(select(User).filter(User.referral_user_id == user_id))
    referred_users = result.scalars().all()
    return [{"user_id": ref.id, "email": ref.email} for ref in referred_users]


@router.delete("/referral/")
async def delete_referral(user_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет реферальный код пользователя."""
    referral = await get_referral_code_by_user_id(db, user_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral code not found")
    await delete_referral_code(db, referral.code)
    await delete_referral_code_from_cache(referral.code)
    return {"user_id": user_id, "message": "Referral code deleted successfully"}
