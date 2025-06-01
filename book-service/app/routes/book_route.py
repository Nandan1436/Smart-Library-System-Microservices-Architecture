from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.schemas.book_schema import *
from app.services.book_service import BookService
from app.database import get_db

router = APIRouter(prefix="/api/books", tags=["Books"])

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)

@router.post("/", response_model=BookCreateResponse, status_code=201)
def create_book(book: BookCreate, book_service: BookService = Depends(get_book_service)):
    return book_service.create_book(book)

@router.get("/", response_model=list[BookResponse])
def search_books(search: Optional[str] = None, book_service: BookService = Depends(get_book_service)):
    return book_service.search_books(search)

@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, book_service: BookService = Depends(get_book_service)):
    return book_service.get_book(id)

@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookInfoUpdate, book_service: BookService = Depends(get_book_service)):
    return book_service.update_book(id, book)

@router.patch("/{id}/availability", response_model=AvailabilityUpdateResponse)
def update_book_availability(id: int, book: BookAvailabilityUpdate, book_service: BookService = Depends(get_book_service)):
    return book_service.update_availability(id, book)

@router.delete("/{id}", status_code=204)
def delete_book(id: int, book_service: BookService = Depends(get_book_service)):
    book_service.delete_book(id)
    return None