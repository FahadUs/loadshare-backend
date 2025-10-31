from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# بيانات التسجيل اللي المستخدم يرسلها
class UserBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    user_type: str  # sender, receiver, driver, admin, support, vendor

class UserCreate(UserBase):
    password: str  # المستخدم يرسل كلمة السر عند التسجيل

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # ضروري في Pydantic v2 لتفعيل ORM Mode