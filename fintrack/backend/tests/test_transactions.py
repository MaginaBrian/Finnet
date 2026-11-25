import pytest

from conftest import register, trade


def test_create_and_list_transactions(client, auth, portfolio_id):
    assert trade(client, auth, portfolio_id).status_code == 201
    res = client.get(f"/api/portfolios/{portfolio_id}/transactions", headers=auth)
    body = res.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["instrument"] == "SCOM"


@pytest.mark.parametrize(
    "payload,field",
    [
        ({"quantity": -5}, "quantity"),
        ({"quantity": 0}, "quantity"),
        ({"quantity": "abc"}, "quantity"),
        ({"unit_price": -1}, "unit_price"),
        ({"type": "HOLD"}, "type"),
        ({"instrument": "bad ticker!"}, "instrument"),
        ({"trade_date": "2999-01-01"}, "trade_date"),
        ({"trade_date": "not-a-date"}, "trade_date"),
    ],
)
def test_invalid_transaction_rejected(client, auth, portfolio_id, payload, field):
    base = {"instrument": "SCOM", "type": "BUY", "quantity": 10, "unit_price": 5, "trade_date": "2026-01-05"}
    res = client.post(f"/api/portfolios/{portfolio_id}/transactions", headers=auth, json={**base, **payload})
    assert res.status_code == 400
    assert field in res.get_json()["error"]["details"]


def test_cannot_sell_more_than_held(client, auth, portfolio_id):
    trade(client, auth, portfolio_id, qty=100)
    res = trade(client, auth, portfolio_id, kind="SELL", qty=101, day="2026-02-01")
    assert res.status_code == 422
    assert res.get_json()["error"]["code"] == "insufficient_holdings"


def test_backdated_sell_before_buy_is_rejected(client, auth, portfolio_id):
    trade(client, auth, portfolio_id, qty=100, day="2026-03-01")
    res = trade(client, auth, portfolio_id, kind="SELL", qty=10, day="2026-02-01")
    assert res.status_code == 422


def test_transactions_on_unknown_portfolio_404(client, auth):
    assert trade(client, auth, 12345).status_code == 404


def test_summary_average_cost_and_pl(client, auth, portfolio_id):
    trade(client, auth, portfolio_id, qty=100, price=10, day="2026-01-05")
    trade(client, auth, portfolio_id, qty=100, price=20, day="2026-01-06")
    trade(client, auth, portfolio_id, kind="SELL", qty=50, price=30, day="2026-01-07")

    summary = client.get(f"/api/portfolios/{portfolio_id}/summary", headers=auth).get_json()
    holding = summary["holdings"][0]
    assert holding["net_quantity"] == 150
    assert holding["average_cost"] == 15
    assert holding["total_invested"] == 2250
    assert holding["total_value"] == 4500
    assert summary["totals"]["realized_pl"] == 750
    assert summary["totals"]["unrealized_pl"] == 2250
    assert summary["totals"]["unrealized_pl_pct"] == 100


def test_fully_sold_position_is_not_listed(client, auth, portfolio_id):
    trade(client, auth, portfolio_id, qty=10, price=5)
    trade(client, auth, portfolio_id, kind="SELL", qty=10, price=6, day="2026-01-06")
    summary = client.get(f"/api/portfolios/{portfolio_id}/summary", headers=auth).get_json()
    assert summary["holdings"] == []
    assert summary["totals"]["realized_pl"] == 10


def test_delete_transaction(client, auth, portfolio_id):
    txn_id = trade(client, auth, portfolio_id).get_json()["id"]
    assert client.delete(f"/api/transactions/{txn_id}", headers=auth).status_code == 204
    assert client.delete(f"/api/transactions/{txn_id}", headers=auth).status_code == 404


def test_cannot_delete_buy_that_backs_a_sell(client, auth, portfolio_id):
    buy_id = trade(client, auth, portfolio_id, qty=100).get_json()["id"]
    trade(client, auth, portfolio_id, kind="SELL", qty=60, day="2026-02-01")
    res = client.delete(f"/api/transactions/{buy_id}", headers=auth)
    assert res.status_code == 409
    assert res.get_json()["error"]["code"] == "ledger_conflict"


def test_other_analyst_cannot_delete_transaction(client, auth, portfolio_id):
    txn_id = trade(client, auth, portfolio_id).get_json()["id"]
    other = register(client, username="intruder")
    assert client.delete(f"/api/transactions/{txn_id}", headers=other).status_code == 404


def test_filter_sort_and_paginate(client, auth, portfolio_id):
    for i in range(5):
        trade(client, auth, portfolio_id, qty=10 + i, day=f"2026-01-0{i + 1}")
    trade(client, auth, portfolio_id, instrument="KCB", qty=5, day="2026-01-09")
    url = f"/api/portfolios/{portfolio_id}/transactions"

    res = client.get(f"{url}?instrument=kcb", headers=auth).get_json()
    assert res["meta"]["total"] == 1

    res = client.get(f"{url}?sort=quantity&order=asc&per_page=2&page=2", headers=auth).get_json()
    assert res["meta"]["pages"] == 3
    assert len(res["data"]) == 2

    assert client.get(f"{url}?sort=bogus", headers=auth).status_code == 400


def test_csv_export(client, auth, portfolio_id):
    trade(client, auth, portfolio_id)
    res = client.get(f"/api/portfolios/{portfolio_id}/transactions/export.csv", headers=auth)
    assert res.status_code == 200
    assert res.mimetype == "text/csv"
    assert res.data.decode().splitlines()[0].startswith("trade_date,instrument")


def test_docs_and_health_are_public(client):
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/docs").status_code == 200
    assert b"openapi" in client.get("/api/openapi.yaml").data
