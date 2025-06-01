from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.schemas.book_schema import *
from fastapi import HTTPException
from datetime import datetime

class BookService:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate) -> BookCreateResponse:
        if self.db.query(Book).filter(Book.isbn == book.isbn).first():
            raise HTTPException(status_code=400, detail="ISBN already registered")
        db_book = Book(**book.dict(), available_copies=book.copies)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return BookCreateResponse.from_orm(db_book)

    def get_book(self, book_id: int) -> BookResponse:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookResponse.from_orm(book)

    def update_book(self, book_id: int, book_update: BookInfoUpdate) -> BookResponse:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book_update.dict(exclude_unset=True)
        if "copies" in update_data:
            new_copies = update_data["copies"]
            if new_copies < book.available_copies:
                raise HTTPException(
                    status_code=400,
                    detail=f"New total copies ({new_copies}) cannot be less than currently available copies ({book.available_copies})."
                )
            copies_delta = max(0,new_copies - book.copies)
            book.copies = new_copies
            book.available_copies += copies_delta

        
            if book.available_copies < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Available copies cannot be negative after update"
                )
            
        for key, value in update_data.items():
            if key != "copies":
                setattr(book, key, value)

        self.db.commit()
        self.db.refresh(book)
        return BookResponse.from_orm(book)

    def update_availability(self, book_id: int, book_update: BookAvailabilityUpdate) -> AvailabilityUpdateResponse:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        if book_update.operation == OperationEnum.increment:
            if book.copies < book.available_copies + book_update.available_copies:
                raise HTTPException(status_code=400, detail="Available copies cannot be greater than total copies")
            book.available_copies += book_update.available_copies
        elif book_update.operation == OperationEnum.decrement:
            if book.available_copies < book_update.available_copies:
                raise HTTPException(status_code=400, detail="Insufficient available copies")
            book.available_copies -= book_update.available_copies
        self.db.commit()
        self.db.refresh(book)
        return AvailabilityUpdateResponse.from_orm(book)

    def delete_book(self, book_id: int) -> None:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        self.db.delete(book)
        self.db.commit()
    
    def search_books(self, search: str) -> list[BookResponse]:
        query = self.db.query(Book).filter(
            (Book.title.ilike(f"%{search}%")) | (Book.author.ilike(f"%{search}%"))
        ).all()
        return [BookResponse.from_orm(book) for book in query]