from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_subscribe_customer():
    response = client.post("/subscribe", json={"customer_number": "999999999"})
    assert response.status_code == 200
    assert response.json() == {"message": "Customer subscribed successfully"}
