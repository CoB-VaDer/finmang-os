from datetime import date, timedelta
from conftest import client, seed

def test_health():
    assert client.get("/health").status_code == 200

def test_account_category_and_transaction_flow():
    a, inc, exp = seed()
    r = client.get("/api/v1/accounts")
    assert r.status_code == 200
    assert r.json()["data"][0]["balance"] == "0.00"
    assert client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(inc.id), "amount": "5000.00", "type": "INCOME", "transaction_date": str(date.today())}).status_code == 201
    assert client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(exp.id), "amount": "1200.00", "type": "EXPENSE", "transaction_date": str(date.today())}).status_code == 201
    assert client.get("/api/v1/balance").json()["data"]["balance"] == "3800.00"

def test_invalid_amount_and_future_date():
    a, inc, _ = seed()
    bad = client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(inc.id), "amount": "0", "type": "INCOME", "transaction_date": str(date.today())})
    assert bad.status_code == 422
    future = client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(inc.id), "amount": "10.00", "type": "INCOME", "transaction_date": str(date.today()+timedelta(days=1))})
    assert future.status_code == 422

def test_category_mismatch_and_inactive_account():
    a, inc, exp = seed()
    bad = client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(exp.id), "amount": "10.00", "type": "INCOME", "transaction_date": str(date.today())})
    assert bad.status_code == 422
    assert bad.json()["error"]["code"] == "CATEGORY_TYPE_MISMATCH"
    client.delete(f"/api/v1/accounts/{a.id}")
    bad2 = client.post("/api/v1/transactions", json={"account_id": str(a.id), "category_id": str(inc.id), "amount": "10.00", "type": "INCOME", "transaction_date": str(date.today())})
    assert bad2.status_code == 409
