from fastapi.testclient import TestClient
from app.main import app
from base64 import b64encode

client = TestClient(app)


def test_get_transactions():
    # First, subscribe and create a loan to generate transaction data
    customer_number = "777777777"
    client.post("/subscribe", json={"customer_number": customer_number})
    client.post("/loan", json={"customer_number": customer_number, "amount": 1000})

    # Prepare Basic Auth header
    user_pass = "lmsuser:lmspass"
    encoded = b64encode(user_pass.encode()).decode("utf-8")
    headers = {"Authorization": f"Basic {encoded}"}

    # Call transaction endpoint
    response = client.get(f"/transactions/{customer_number}", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "accountNumber" in response.json()[0]
