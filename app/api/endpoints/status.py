from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.schemas import Loan

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{customer_number}")
def get_loan_status(customer_number: str, db: Session = Depends(get_db)):
    loan = (
        db.query(Loan)
        .filter_by(customer_number=customer_number)
        .order_by(Loan.id.desc())
        .first()
    )

    if not loan:
        raise HTTPException(
            status_code=404, detail="No loan record found for this customer"
        )

    return {
        "customer_number": loan.customer_number,
        "amount": loan.amount,
        "status": loan.status,
        "score": loan.score,
        "limit_amount": loan.limit_amount,
    }
