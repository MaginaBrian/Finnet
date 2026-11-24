def _auth_header(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Grace Hopper", "email": "grace@example.com", "password": "secret123"},
    )
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_portfolio_transaction_and_summary(client):
    headers = _auth_header(client)
    created = client.post(
        "/api/portfolios",
        json={"name": "Growth", "description": "Equities"},
        headers=headers,
    )
    assert created.status_code == 201
    portfolio_id = created.get_json()["data"]["id"]

    deposit = client.post(
        f"/api/portfolios/{portfolio_id}/transactions",
        json={"kind": "deposit", "amount": "1000", "occurred_at": "2026-01-01"},
        headers=headers,
    )
    assert deposit.status_code == 201

    buy = client.post(
        f"/api/portfolios/{portfolio_id}/transactions",
        json={
            "kind": "buy",
            "symbol": "aapl",
            "quantity": "2",
            "price": "100",
            "occurred_at": "2026-01-02",
        },
        headers=headers,
    )
    assert buy.status_code == 201
    assert buy.get_json()["data"]["symbol"] == "AAPL"

    short = client.post(
        f"/api/portfolios/{portfolio_id}/transactions",
        json={
            "kind": "sell",
            "symbol": "AAPL",
            "quantity": "5",
            "price": "110",
            "occurred_at": "2026-01-03",
        },
        headers=headers,
    )
    assert short.status_code == 400

    summary = client.get("/api/summary", headers=headers)
    body = summary.get_json()["data"]
    assert summary.status_code == 200
    assert body["portfolio_count"] == 1
    assert body["cash"] == 800
    assert body["holdings_value"] == 200
    assert body["net_worth"] == 1000
