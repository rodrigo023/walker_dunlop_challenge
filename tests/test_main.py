from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)


def test_preferences_get_preferences():
    response = client.get("/preferences/")
    assert response.status_code == 200
