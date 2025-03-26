from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.schemas import Loan
from app.core.security import verify_credentials

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{customer_number}")
def get_transactions(
    customer_number: str,
    auth: bool = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    loan = (
        db.query(Loan)
        .filter_by(customer_number=customer_number)
        .order_by(Loan.id.desc())
        .first()
    )

    if not loan or not loan.transaction_data:
        raise HTTPException(status_code=404, detail="No transaction data available")

    return loan.transaction_data
