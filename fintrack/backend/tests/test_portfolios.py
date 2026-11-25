from conftest import register


def test_portfolio_crud(client, auth):
    body = {"name": "Growth", "client_name": "Baraka Ltd", "base_currency": "KES"}
    created = client.post("/api/portfolios", headers=auth, json=body)
    assert created.status_code == 201
    pid = created.get_json()["id"]

    assert len(client.get("/api/portfolios", headers=auth).get_json()["data"]) == 1
    assert client.get(f"/api/portfolios/{pid}", headers=auth).get_json()["name"] == "Growth"

    updated = client.put(f"/api/portfolios/{pid}", headers=auth, json={**body, "base_currency": "USD"})
    assert updated.status_code == 200
    assert updated.get_json()["base_currency"] == "USD"

    assert client.delete(f"/api/portfolios/{pid}", headers=auth).status_code == 204
    assert client.get(f"/api/portfolios/{pid}", headers=auth).status_code == 404


def test_invalid_currency_and_missing_fields(client, auth):
    res = client.post("/api/portfolios", headers=auth, json={"name": "", "base_currency": "EUR"})
    assert res.status_code == 400
    details = res.get_json()["error"]["details"]
    assert set(details) == {"name", "client_name", "base_currency"}


def test_unknown_portfolio_is_404_with_json_body(client, auth):
    res = client.get("/api/portfolios/999", headers=auth)
    assert res.status_code == 404
    assert res.get_json()["error"]["code"] == "not_found"


def test_cannot_see_another_analysts_portfolio(client, portfolio_id):
    other = register(client, username="intruder")
    assert client.get(f"/api/portfolios/{portfolio_id}", headers=other).status_code == 404
    assert client.delete(f"/api/portfolios/{portfolio_id}", headers=other).status_code == 404
    assert client.get("/api/portfolios", headers=other).get_json()["data"] == []


def test_non_json_body_is_400(client, auth):
    res = client.post("/api/portfolios", headers=auth, data="oops", content_type="text/plain")
    assert res.status_code == 400
    assert res.get_json()["error"]["code"] == "invalid_json"
