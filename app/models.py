from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(Date, default=date.today)
    referral_user_id = Column(Integer, ForeignKey(
        "users.id"), nullable=True)

    referrals = relationship("ReferralCode", back_populates="owner")
    referred_by = relationship("User", remote_side=[
                               id], back_populates="referred_users")
    referred_users = relationship(
        "User", back_populates="referred_by")


class ReferralCode(Base):
    """Модель реферального кода."""
    __tablename__ = "referral_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(Date, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="referrals")
