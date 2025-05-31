from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user_route

# Initialize the FastAPI application
app = FastAPI()

# Create database tables (optional if already done via init_db.py)
Base.metadata.create_all(bind=engine)

# Include the user routes
app.include_router(user_route.router)