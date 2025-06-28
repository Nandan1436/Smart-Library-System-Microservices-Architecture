from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate,UserCreateResponse,UserResponse
from fastapi import HTTPException
from app.schemas.user_schema import UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: UserCreate) -> UserCreateResponse:
        if self.db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserCreateResponse.from_orm(db_user)

    async def get_user(self, user_id: int) -> UserResponse:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.from_orm(user)
    
    