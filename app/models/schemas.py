from sqlalchemy import Column, Integer, String, Float
from app.models.database import Base
from pydantic import BaseModel
from sqlalchemy import JSON


class CustomerCreate(BaseModel):
    customer_number: str


class LoanRequest(BaseModel):
    customer_number: str
    amount: float


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_number = Column(String, unique=True, index=True)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    customer_number = Column(String, index=True)
    amount = Column(Float)
    status = Column(String, default="PENDING")  # PENDING, APPROVED, FAILED
    score = Column(Integer, nullable=True)
    limit_amount = Column(Float, nullable=True)
    retries_left = Column(Integer)
    token = Column(String, nullable=True)
    kyc_data = Column(JSON, nullable=True)
    transaction_data = Column(JSON, nullable=True)
