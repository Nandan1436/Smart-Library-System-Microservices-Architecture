from pydantic import BaseModel,Field,ConfigDict,EmailStr
from typing import Optional,List
from datetime import datetime

class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class LoanReturn(BaseModel):
    loan_id: int

class LoanExtend(BaseModel):
    extension_days: int

class LoanResponse(BaseModel):
    id: int
    user_id: int
    book_id: int 
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True 

class UserInLoan(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True 

class BookInLoan(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        from_attributes = True 

class LoanDetailResponse(BaseModel):
    id: int
    user: UserInLoan
    book: BookInLoan
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True 

class LoanHistoryResponse(BaseModel):
    loan: List[LoanDetailResponse]
    total: int

    class Config:
        from_attributes = True 
