from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os,pathlib
from dotenv import load_dotenv

env_path = pathlib.Path(__file__).parent.parent / ".env"
print("Looking for .env at:", env_path)
load_dotenv(dotenv_path=env_path)


DATABASE_URL = os.getenv("USER_DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)   # <-- debug line

engine = create_engine(DATABASE_URL, echo=True) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()