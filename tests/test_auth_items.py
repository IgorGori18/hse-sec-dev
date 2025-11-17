from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_and_login(username: str, password: str) -> str:
    r = client.post("/auth/register", json={"username": username, "password": password})
    assert r.status_code in (200, 201)
    token = r.json()["access_token"]
    return token


def test_register_and_login_ok():
    token = register_and_login("user1", "password123")
    assert isinstance(token, str)


def test_login_wrong_password():
    register_and_login("user2", "password123")
    r = client.post("/auth/login", json={"username": "user2", "password": "wrong"})
    assert r.status_code == 401
    body = r.json()
    assert body["code"] == "AUTH_FAILED"


def test_create_item_requires_auth():
    r = client.post("/api/v1/items", json={"title": "task1"})
    assert r.status_code == 401
    body = r.json()
    assert body["code"] == "UNAUTHORIZED"


def test_owner_can_access_own_item():
    token = register_and_login("owner", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/api/v1/items", json={"title": "own-task"}, headers=headers)
    assert r.status_code == 201
    item_id = r.json()["id"]

    r2 = client.get(f"/api/v1/items/{item_id}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["title"] == "own-task"


def test_other_user_cannot_access_foreign_item():
    token_owner = register_and_login("owner2", "password123")
    h_owner = {"Authorization": f"Bearer {token_owner}"}
    r = client.post("/api/v1/items", json={"title": "secret"}, headers=h_owner)
    item_id = r.json()["id"]

    token_other = register_and_login("intruder", "password123")
    h_other = {"Authorization": f"Bearer {token_other}"}

    r2 = client.get(f"/api/v1/items/{item_id}", headers=h_other)
    assert r2.status_code == 403
    body = r2.json()
    assert body["code"] == "FORBIDDEN"


def test_items_pagination():
    token = register_and_login("pager", "password123")
    headers = {"Authorization": f"Bearer {token}"}
    for i in range(5):
        client.post("/api/v1/items", json={"title": f"t{i}"}, headers=headers)

    r = client.get("/api/v1/items?limit=2&offset=1", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
