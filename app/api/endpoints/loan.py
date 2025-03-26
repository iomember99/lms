import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.schemas import LoanRequest, Loan, Customer
from app.core.config import settings
from app.core.scoring import (
    register_transaction_endpoint_mock,
    initiate_scoring_mock,
    poll_score_and_update_mock,
)
from app.core.soap_clients import (
    fetch_kyc_mock,
    fetch_transactions_mock,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def request_loan(
    request: LoanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # check if customer exists
    customer = (
        db.query(Customer).filter_by(customer_number=request.customer_number).first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # get loans that are pending or approved
    existing_loan = (
        db.query(Loan)
        .filter(
            Loan.customer_number == request.customer_number,
            Loan.status.in_(["PENDING", "APPROVED"]),
        )
        .first()
    )

    # if either pending or approved loan exists, return error
    if existing_loan:
        raise HTTPException(
            status_code=400, detail="Customer already has an active or pending loan"
        )

    # otherwise make a loan request
    new_loan = Loan(
        customer_number=request.customer_number,
        amount=request.amount,
        status="PENDING",
        retries_left=settings.RETRY_LIMIT,
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    logging.info(
        f"Loan request created: customer={request.customer_number}, amount={request.amount}"
    )

    # Fetch and store KYC data
    kyc_data = fetch_kyc_mock(request.customer_number)
    if not kyc_data:
        raise HTTPException(
            status_code=503,
            detail="We couldn't process your loan request at the moment. Please try again later.",
        )

    new_loan.kyc_data = kyc_data
    db.commit()

    # Fetch transaction history
    trx_data = fetch_transactions_mock(request.customer_number)
    if not trx_data:
        raise HTTPException(
            status_code=503,
            detail="We couldn't process your loan request at the moment. Please try again later.",
        )
    new_loan.transaction_data = trx_data
    db.commit()

    try:
        client_token = await register_transaction_endpoint_mock()
    except Exception as e:
        logging.error(
            f"Registration with scoring engine failed for customer {request.customer_number}: {e}"
        )
        raise HTTPException(
            status_code=503,
            detail="We couldn't process your request at the moment. Please try again later.",
        )

    # initiate scoring asynchronously
    scoring_token = await initiate_scoring_mock(request.customer_number, client_token)
    background_tasks.add_task(
        poll_score_and_update_mock,
        db,
        request.customer_number,
        scoring_token,
        settings.RETRY_LIMIT,
        client_token,
    )

    return {"message": "Loan request received. Scoring in progress."}
