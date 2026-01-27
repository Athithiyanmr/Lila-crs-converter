from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in (200, 404)

def test_docs():
    response = client.get("/docs")
    assert response.status_code in (200, 302)
