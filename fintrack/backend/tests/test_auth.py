def _register(client, username="ada"):
    response = client.post(
        "/api/auth/register",
        json={"username": username, "full_name": "Ada Lovelace", "password": "secret123"},
    )
    assert response.status_code == 201
    return response.get_json()


def test_register_and_me(client):
    payload = _register(client)
    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {payload['token']}"},
    )
    assert me.status_code == 200
    assert me.get_json()["user"]["username"] == "ada"


def test_login_rejects_bad_password(client):
    _register(client)
    response = client.post(
        "/api/auth/login",
        json={"username": "ada", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_duplicate_username_is_rejected(client):
    _register(client)
    response = client.post(
        "/api/auth/register",
        json={"username": "ada", "full_name": "Ada", "password": "secret123"},
    )
    assert response.status_code == 409
