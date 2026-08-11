from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_expense():
    response = client.post("/expenses", json={
        "amount": 100,
        "category": "food",
        "date": "2026-08-11"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["amount"] == 100
    assert data["data"]["category"] == "food"

def test_create_expense_rejects_negative_amount():
    response = client.post("/expenses", json={
        "amount": -50,
        "category": "food",
        "date": "2026-08-11"
    })
    assert response.status_code == 422  # validation error

def test_get_expenses():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_monthly_summary():
    response = client.get("/expenses/summary/monthly")
    assert response.status_code == 200
    assert isinstance(response.json(), list)