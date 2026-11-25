import pytest

from app import create_app
from app.extensions import db
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username="analyst", password="password123"):
    res = client.post("/api/auth/register", json={"username": username, "password": password})
    assert res.status_code == 201, res.get_json()
    return {"Authorization": f"Bearer {res.get_json()['token']}"}


@pytest.fixture()
def auth(client):
    return register(client)


@pytest.fixture()
def portfolio_id(client, auth):
    res = client.post(
        "/api/portfolios", headers=auth,
        json={"name": "Growth", "client_name": "Baraka Ltd", "base_currency": "KES"},
    )
    return res.get_json()["id"]


def trade(client, auth, pid, kind="BUY", qty=100, price=10, day="2026-01-05", instrument="SCOM"):
    return client.post(
        f"/api/portfolios/{pid}/transactions", headers=auth,
        json={"instrument": instrument, "type": kind, "quantity": qty, "unit_price": price, "trade_date": day},
    )
