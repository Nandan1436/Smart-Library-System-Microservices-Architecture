from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanReturn, LoanResponse, LoanDetailResponse, LoanHistoryResponse
from app.services.loan_service import LoanService
from app.database import get_db

router = APIRouter(prefix="/api/loans", tags=["Loans"])

def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    return LoanService(db)

@router.post("/", response_model=LoanResponse, status_code=201)
async def create_loan(loan: LoanCreate, loan_service: LoanService = Depends(get_loan_service)):
    return await loan_service.issue_book(loan)

@router.post("/returns", response_model=LoanResponse)
async def return_book(loan_return: LoanReturn, loan_service: LoanService = Depends(get_loan_service)):
    return await loan_service.return_book(loan_return)

@router.get("/user/{user_id}", response_model=LoanHistoryResponse)
async def get_user_loans(user_id: int, loan_service: LoanService = Depends(get_loan_service)):
    return await loan_service.get_user_loans(user_id)

@router.get("/{id}", response_model=LoanDetailResponse)
async def get_loan(id: int, loan_service: LoanService = Depends(get_loan_service)):
    return await loan_service.get_loan(id)