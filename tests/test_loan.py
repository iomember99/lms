from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_request_loan():
    # First, subscribe the customer
    client.post("/subscribe", json={"customer_number": "888888888"})

    # Then, request a loan
    response = client.post(
        "/loan", json={"customer_number": "888888888", "amount": 1500}
    )

    assert response.status_code == 200
    assert "message" in response.json()
    assert "Loan request received. Scoring in progress." in response.json()["message"]
