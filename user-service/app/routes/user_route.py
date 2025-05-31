from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserCreateResponse
from app.services.user_service import UserService
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/", response_model=UserCreateResponse, status_code=201)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user(id)

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(id, user)