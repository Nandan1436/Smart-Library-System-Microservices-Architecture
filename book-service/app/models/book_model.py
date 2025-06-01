from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False, index=True)
    author = Column(String(250), nullable=False, index=True)
    isbn = Column(String(13), unique=True, nullable=False)
    copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
