def _auth_header(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "grace", "full_name": "Grace Hopper", "password": "secret123"},
    )
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_portfolio_transaction_and_summary(client):
    headers = _auth_header(client)
    created = client.post(
        "/api/portfolios",
        json={"name": "Growth", "client_name": "Ada Capital", "base_currency": "KES"},
        headers=headers,
    )
    assert created.status_code == 201
    portfolio_id = created.get_json()["id"]

    buy = client.post(
        f"/api/portfolios/{portfolio_id}/transactions",
        json={
            "instrument": "scom",
            "type": "BUY",
            "quantity": "2",
            "unit_price": "100",
            "trade_date": "2026-01-02",
        },
        headers=headers,
    )
    assert buy.status_code == 201
    assert buy.get_json()["instrument"] == "SCOM"

    short = client.post(
        f"/api/portfolios/{portfolio_id}/transactions",
        json={
            "instrument": "SCOM",
            "type": "SELL",
            "quantity": "5",
            "unit_price": "110",
            "trade_date": "2026-01-03",
        },
        headers=headers,
    )
    assert short.status_code == 422
    assert short.get_json()["error"]["code"] == "insufficient_holdings"

    summary = client.get(f"/api/portfolios/{portfolio_id}/summary", headers=headers)
    totals = summary.get_json()["totals"]
    assert summary.status_code == 200
    assert totals["total_invested"] == 200
    assert totals["total_value"] == 200
    assert totals["unrealized_pl"] == 0
