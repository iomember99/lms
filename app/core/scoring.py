import httpx
import asyncio
import logging
from app.core.config import settings
from app.models import schemas
from sqlalchemy.orm import Session


# NOTE: Real integration logic below is currently unused
# due to unresponsive external services. Mock version used during assessment.
async def initiate_scoring(customer_number: str, token: str) -> str:
    url = f"{settings.SCORING_BASE_URL}/scoring/initiateQueryScore/{customer_number}"
    headers = {"client-token": token}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # return scoring token
        return response.text


# NOTE: Real integration logic below is currently unused
# due to unresponsive external services. Mock version used during assessment.
async def poll_score_and_update(
    db: Session,
    customer_number: str,
    scoring_token: str,
    retries: int,
    client_token: str,
):
    url = f"{settings.SCORING_BASE_URL}/scoring/queryScore/{scoring_token}"
    headers = {"client-token": client_token}

    for attempt in range(retries):
        await asyncio.sleep(5)  # wait before each retry
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            score = data.get("score")
            limit = data.get("limitAmount")

            loan = (
                db.query(schemas.Loan)
                .filter_by(customer_number=customer_number, status="PENDING")
                .first()
            )
            if loan:
                if limit >= loan.amount:
                    loan.status = "APPROVED"
                else:
                    loan.status = "FAILED"
                loan.score = score
                loan.limit_amount = limit
                db.commit()
                return
            logging.info(
                f"Scoring result: customer={customer_number}, score={score}, limit={limit}"
            )

    # If all retries fail, mark the loan request status as failed
    loan = (
        db.query(schemas.Loan)
        .filter_by(customer_number=customer_number, status="PENDING")
        .first()
    )
    if loan:
        loan.status = "FAILED"
        db.commit()
    logging.warning(
        f"Scoring retries exhausted for {customer_number}. Marking loan as FAILED."
    )


# NOTE: Real integration logic below is currently unused
# due to unresponsive external services. Mock version used during assessment.
async def register_transaction_endpoint():
    url = f"{settings.SCORING_BASE_URL}/client/createClient"
    print(f"url is {url}")
    payload = {
        "url": "https://d5ad-105-163-0-149.ngrok-free.app/transactions/{customerNumber}",
        "name": settings.CLIENT_NAME,
        "username": settings.CLIENT_USERNAME,
        "password": settings.CLIENT_PASSWORD,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                logging.info("Scoring engine registration successful.")
                return token
            else:
                logging.error(
                    f"Registration failed with status {response.status_code}: {response.text}"
                )
                raise Exception("Failed to register with scoring engine")

        except Exception as e:
            logging.exception(
                f"Exception occurred during scoring engine registration, {e}"
            )
            raise


async def register_transaction_endpoint_mock():
    logging.warning("[MOCK] Scoring endpoint registration simulated.")
    return "mock-client-token-123456"


async def initiate_scoring_mock(customer_number: str, token: str) -> str:
    logging.warning(f"[MOCK] Initiating scoring for {customer_number}")
    return "mock-score-token-abc123"


async def poll_score_and_update_mock(
    db: Session,
    customer_number: str,
    scoring_token: str,
    retries: int,
    client_token: str,
):
    logging.warning(
        f"[MOCK] Polling scoring engine for {customer_number} using token {scoring_token}"
    )

    # simulate waiting
    await asyncio.sleep(5)

    score = 720
    limit = 5000

    loan = (
        db.query(schemas.Loan)
        .filter_by(customer_number=customer_number, status="PENDING")
        .first()
    )
    if loan:
        if limit >= loan.amount:
            loan.status = "APPROVED"
        else:
            loan.status = "FAILED"
        loan.score = score
        loan.limit_amount = limit
        db.commit()
        logging.info(
            f"[MOCK] Scoring complete for {customer_number}: score={score}, limit={limit}"
        )
