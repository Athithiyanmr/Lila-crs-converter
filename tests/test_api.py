from fastapi.testclient import TestClient

# adjust this import if your app file name is different
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code in (200, 404)