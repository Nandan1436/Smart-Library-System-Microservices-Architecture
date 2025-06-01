from app.database import Base,engine
from app.models.book_model import Book

Base.metadata.create_all(bind=engine)
