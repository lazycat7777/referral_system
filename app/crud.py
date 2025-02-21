from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, ReferralCode
from datetime import datetime
from .auth import hash_password

async def get_user_by_email(db: AsyncSession, email: str):
    """Возвращает пользователя по email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str):
    """Создает нового пользователя."""
    hashed_password = hash_password(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_referral_code(db: AsyncSession, user_id: int, code: str, expires_at: datetime):
    """Создает реферальный код для пользователя."""
    existing_code = await db.execute(select(ReferralCode).filter(ReferralCode.owner_id == user_id))
    if existing_code.scalars().first():
        return None
    referral_code = ReferralCode(code=code, owner_id=user_id, expires_at=expires_at)
    db.add(referral_code)
    await db.commit()
    await db.refresh(referral_code)
    return referral_code

async def get_referral_code_by_email(db: AsyncSession, email: str):
    """Возвращает реферальный код по email пользователя."""
    result = await db.execute(select(ReferralCode).join(User).filter(User.email == email))
    return result.scalars().first()

async def get_referrals_by_user_id(db: AsyncSession, user_id: int):
    """Возвращает список реферальных кодов пользователя."""
    result = await db.execute(select(ReferralCode).filter(ReferralCode.owner_id == user_id))
    return result.scalars().all()