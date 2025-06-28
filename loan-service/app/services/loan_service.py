from sqlalchemy.orm import Session
from app.models.loan_model import Loan
from app.schemas.loan_schema import *
from fastapi import HTTPException
from datetime import datetime
import requests
import os

class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service_url = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
        self.book_service_url = os.getenv("BOOK_SERVICE_URL", "http://localhost:8001")

    def issue_book(self, loan: LoanCreate) -> LoanResponse:
        try:
            user_response = requests.get(f"{self.user_service_url}/api/users/{loan.user_id}")
            if user_response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            user_response.raise_for_status()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="User Service unavailable")
        try:
            book_response = requests.get(f"{self.book_service_url}/api/books/{loan.book_id}")
            if book_response.status_code == 404:
                raise HTTPException(status_code=400, detail="Book not found")
            book_response.raise_for_status()
            book_data = book_response.json()
            if book_data["available_copies"] <= 0:
                raise HTTPException(status_code=400, detail="No available copies of the book")
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="Book Service unavailable")
        try:
            availability_response = requests.patch(
                f"{self.book_service_url}/api/books/{loan.book_id}/availability",
                json={"available_copies": 1, "operation": "decrement"}
            )
            availability_response.raise_for_status()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="Book Service unavailable")
        db_loan = Loan(
            user_id=loan.user_id,
            book_id=loan.book_id,
            due_date=loan.due_date,
            issue_date=datetime.utcnow(),
            status="ACTIVE"
        )
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return LoanResponse.from_orm(db_loan)

    def return_book(self, loan_return: LoanReturn) -> LoanResponse:
        db_loan = self.db.query(Loan).filter(Loan.id == loan_return.loan_id).first()
        if not db_loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if db_loan.status == "RETURNED":
            raise HTTPException(status_code=400, detail="Loan already returned")
        try:
            availability_response = requests.patch(
                f"{self.book_service_url}/api/books/{db_loan.book_id}/availability",
                json={"available_copies": 1, "operation": "increment"}
            )
            availability_response.raise_for_status()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="Book Service unavailable")


        db_loan.status = "RETURNED"
        db_loan.return_date = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_loan)
        return LoanResponse.from_orm(db_loan)

    
    def get_loan(self, loan_id: int) -> LoanDetailResponse:
        db_loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if not db_loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        try:
            user_response = requests.get(f"{self.user_service_url}/api/users/{db_loan.user_id}")
            user_response.raise_for_status()
            user_data = user_response.json()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="User Service unavailable")

        try:
            book_response = requests.get(f"{self.book_service_url}/api/books/{db_loan.book_id}")
            book_response.raise_for_status()
            book_data = book_response.json()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="Book Service unavailable")

        return LoanDetailResponse(
            id=db_loan.id,
            user=UserInLoan(**user_data),
            book=BookInLoan(**book_data),
            issue_date=db_loan.issue_date,
            due_date=db_loan.due_date,
            return_date=db_loan.return_date,
            status=db_loan.status
        )

    def get_user_loans(self, user_id: int) -> LoanHistoryResponse:
        try:
            user_response = requests.get(f"{self.user_service_url}/api/users/{user_id}")
            if user_response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            user_response.raise_for_status()
            user_data = user_response.json()
        except requests.RequestException:
            raise HTTPException(status_code=503, detail="User Service unavailable")

        loans = self.db.query(Loan).filter(Loan.user_id == user_id).all()
        loan_details = []

        for loan in loans:
            try:
                book_response = requests.get(f"{self.book_service_url}/api/books/{loan.book_id}")
                book_response.raise_for_status()
                book_data = book_response.json()
            except requests.RequestException:
                raise HTTPException(status_code=503, detail="Book Service unavailable")

            loan_details.append(
                LoanDetailResponse(
                    id=loan.id,
                    user=UserInLoan(**user_data),
                    book=BookInLoan(**book_data),
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    return_date=loan.return_date,
                    status=loan.status
                )
            )

        return LoanHistoryResponse(loan=loan_details, total=len(loan_details))