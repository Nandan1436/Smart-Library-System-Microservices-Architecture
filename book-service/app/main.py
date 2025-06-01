from fastapi import FastAPI
from app.database import Base, engine
from app.routes import book_route

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(book_route.router)