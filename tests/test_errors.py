from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_item():
    r = client.post("/auth/register", json={"username": "u1", "password": "p"})
    assert r.status_code in (200, 201)
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    r2 = client.get("/api/v1/items/999", headers=headers)
    assert r2.status_code == 404
    body = r2.json()
    assert body["code"] == "NOT_FOUND"
    assert body["message"] == "item not found"


def test_validation_error():
    r = client.post("/auth/register", json={"username": "u2", "password": "p"})
    assert r.status_code in (200, 201)
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    r2 = client.post("/api/v1/items", json={"title": ""}, headers=headers)

    assert r2.status_code in (400, 422)

    body = r2.json()
    assert "code" in body
