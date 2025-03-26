from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models import schemas
from app.models.schemas import CustomerCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def subscribe_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(schemas.Customer)
        .filter_by(customer_number=payload.customer_number)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Customer already subscribed")

    new_customer = schemas.Customer(customer_number=payload.customer_number)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer subscribed successfully"}
