def _register(client, email="ada@example.com"):
    response = client.post(
        "/api/auth/register",
        json={"name": "Ada Lovelace", "email": email, "password": "secret123"},
    )
    assert response.status_code == 201
    return response.get_json()["data"]


def test_register_and_me(client):
    payload = _register(client)
    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    assert me.status_code == 200
    assert me.get_json()["data"]["email"] == "ada@example.com"


def test_login_rejects_bad_password(client):
    _register(client)
    response = client.post(
        "/api/auth/login",
        json={"email": "ada@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_duplicate_email_is_rejected(client):
    _register(client)
    response = client.post(
        "/api/auth/register",
        json={"name": "Ada", "email": "ada@example.com", "password": "secret123"},
    )
    assert response.status_code == 409
