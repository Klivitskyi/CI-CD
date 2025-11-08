from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, world!"}


def test_create_and_get_item():
    # create
    r = client.post("/items/", json={"name": "foo", "description": "desc"})
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert data["name"] == "foo"

    # get
    r2 = client.get(f"/items/{data['id']}")
    assert r2.status_code == 200
    assert r2.json() == data
