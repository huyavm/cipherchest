from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
