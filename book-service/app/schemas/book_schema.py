from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
from enum import Enum

class OperationEnum(str, Enum):
    increment = "increment"
    decrement = "decrement"

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class BookInfoUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    copies: Optional[int] = None

class BookAvailabilityUpdate(BaseModel): 
    available_copies: int  
    operation: OperationEnum

class BookCreateResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int
    created_at: datetime

    class Config:
        from_attributes = True 

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 

class AvailabilityUpdateResponse(BaseModel):
    id: int
    available_copies: int
    updated_at: datetime

    class Config:
        from_attributes = True

class BookInLoan(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        from_attributes = True 