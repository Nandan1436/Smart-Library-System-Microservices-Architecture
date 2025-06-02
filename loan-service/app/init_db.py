from app.database import Base, engine
from app.models.loan_model import Loan

Base.metadata.create_all(bind=engine)