from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_referral_code, get_referral_code_by_email, get_referrals_by_user_id
from app.schemas import ReferralCreate, ReferralResponse
from app.redis_cache import get_referral_code_from_cache, set_referral_code_in_cache

router = APIRouter()


@router.post("/referral/create/", response_model=ReferralResponse)
async def create_referral(user_id: int, referral_data: ReferralCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый реферальный код для пользователя."""
    referral = await create_referral_code(db, user_id, referral_data.code, referral_data.expires_at)
    if not referral:
        raise HTTPException(
            status_code=400, detail="User already has an active referral code")
    await set_referral_code_in_cache(user_id, referral.code)
    return {"code": referral.code, "expires_at": referral.expires_at}


@router.get("/referral/{email}", response_model=ReferralResponse)
async def get_referral_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """Возвращает реферальный код по email пользователя."""
    cached_code = await get_referral_code_from_cache(email)
    if cached_code:
        return {"code": cached_code}
    referral = await get_referral_code_by_email(db, email)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral code not found")
    await set_referral_code_in_cache(email, referral.code)
    return {"code": referral.code, "expires_at": referral.expires_at}


@router.get("/referrals/{user_id}", response_model=list[ReferralResponse])
async def get_referrals(user_id: int, db: AsyncSession = Depends(get_db)):
    """Возвращает список реферальных кодов пользователя."""
    referrals = await get_referrals_by_user_id(db, user_id)
    return [{"code": ref.code, "expires_at": ref.expires_at} for ref in referrals]
