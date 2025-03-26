from fastapi import FastAPI
from app.api.endpoints import loan, customer, status, transaction
from app.models.database import Base, engine
from app.core.logging_config import init_logging

app = FastAPI(title="Loan Management System")

app.include_router(customer.router, prefix="/subscribe", tags=["Subscription"])
app.include_router(loan.router, prefix="/loan", tags=["Loan Requests"])
app.include_router(status.router, prefix="/status", tags=["Loan Status"])
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])

Base.metadata.create_all(bind=engine)
init_logging()


@app.get("/")
def read_root():
    return {"message": "LMS API is running!"}
