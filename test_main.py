import os
os.environ["DB_NAME"] = "test_expenses.db"

import pytest
from fastapi.testclient import TestClient
from main import app, API_KEY

client = TestClient(app)
headers = {"x-api-key": API_KEY}

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    if os.path.exists("test_expenses.db"):
        try:
            os.remove("test_expenses.db")
        except PermissionError:
            pass

def test_create_expense():
    response = client.post("/expenses", json={
        "amount": 100,
        "category": "food",
        "date": "2026-08-11"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["amount"] == 100
    assert data["data"]["category"] == "food"

def test_create_expense_rejects_negative_amount():
    response = client.post("/expenses", json={
        "amount": -50,
        "category": "food",
        "date": "2026-08-11"
    }, headers=headers)
    assert response.status_code == 422

def test_create_expense_requires_auth():
    response = client.post("/expenses", json={
        "amount": 100,
        "category": "food",
        "date": "2026-08-11"
    })  # no headers
    assert response.status_code == 401

def test_get_expenses():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)