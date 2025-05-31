from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None

class UserCreateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  

class UserInLoan(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True 
