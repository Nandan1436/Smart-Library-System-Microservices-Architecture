from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanCreate, LoanReturn, LoanResponse, LoanDetailResponse, LoanHistoryResponse
from app.services.loan_service import LoanService
from app.database import get_db

router = APIRouter(prefix="/api/loans", tags=["Loans"])

def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    return LoanService(db)

@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan(loan: LoanCreate, loan_service: LoanService = Depends(get_loan_service)):
    return loan_service.create_loan(loan)

@router.post("/returns", response_model=LoanResponse)
def return_book(loan_return: LoanReturn, loan_service: LoanService = Depends(get_loan_service)):
    return loan_service.return_book(loan_return)

@router.get("/user/{user_id}", response_model=LoanHistoryResponse)
def get_user_loans(user_id: int, loan_service: LoanService = Depends(get_loan_service)):
    return loan_service.get_user_loans(user_id)

@router.get("/{id}", response_model=LoanDetailResponse)
def get_loan(id: int, loan_service: LoanService = Depends(get_loan_service)):
    return loan_service.get_loan(id)