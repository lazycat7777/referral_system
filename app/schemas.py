from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    """Схема для создания пользователя."""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Схема для входа пользователя."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя."""
    user_id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserRegisterWithReferralResponse(BaseModel):
    """Схема для ответа с данными пользователя при регистрации с реферальным кодом."""
    user_id: int
    email: EmailStr
    referral_code: str
    referral_user_id: int

    class Config:
        from_attributes = True


class ReferralCreate(BaseModel):
    """Схема для создания реферального кода."""
    code: str
    expires_at: date


class ReferralResponse(BaseModel):
    """Схема для ответа с данными реферального кода."""
    user_id: int
    code: str
    expires_at: date

    class Config:
        from_attributes = True


class ReferralUserResponse(BaseModel):
    """Схема для ответа с данными пользователя, зарегистрированного по реферальному коду."""
    user_id: int
    email: EmailStr

    class Config:
        from_attributes = True
