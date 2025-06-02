from fastapi import FastAPI
from app.database import Base, engine
from app.routes import loan_route
import os

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(loan_route.router)