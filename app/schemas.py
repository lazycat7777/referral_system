from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """Схема для создания пользователя."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя."""
    email: EmailStr

    class Config:
        from_attributes = True

class ReferralCreate(BaseModel):
    """Схема для создания реферального кода."""
    code: str
    expires_at: datetime

class ReferralResponse(BaseModel):
    """Схема для ответа с данными реферального кода."""
    code: str
    expires_at: datetime

    class Config:
        from_attributes = True