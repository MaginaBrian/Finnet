from conftest import register


def test_register_hashes_password_and_returns_token(client, app):
    register(client)
    from app.models import User

    user = User.query.filter_by(username="analyst").one()
    assert user.password_hash != "password123"
    assert user.check_password("password123")


def test_duplicate_username_conflicts(client):
    register(client)
    res = client.post("/api/auth/register", json={"username": "ANALYST", "password": "password123"})
    assert res.status_code == 409
    assert res.get_json()["error"]["code"] == "conflict"


def test_short_password_rejected_with_details(client):
    res = client.post("/api/auth/register", json={"username": "newuser", "password": "short"})
    assert res.status_code == 400
    body = res.get_json()["error"]
    assert body["code"] == "validation_error"
    assert "password" in body["details"]


def test_login_wrong_password_is_401(client):
    register(client)
    res = client.post("/api/auth/login", json={"username": "analyst", "password": "nope-nope"})
    assert res.status_code == 401


def test_login_success(client):
    register(client)
    res = client.post("/api/auth/login", json={"username": "analyst", "password": "password123"})
    assert res.status_code == 200
    assert res.get_json()["token"]


def test_endpoints_require_token(client):
    for path in ("/api/portfolios", "/api/auth/me"):
        res = client.get(path)
        assert res.status_code == 401
        assert res.get_json()["error"]["code"] == "unauthorized"


def test_garbage_token_rejected(client):
    res = client.get("/api/portfolios", headers={"Authorization": "Bearer not.a.jwt"})
    assert res.status_code == 401
