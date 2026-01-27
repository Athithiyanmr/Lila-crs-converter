import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code in (200, 404)


def test_docs():
    r = client.get("/docs")
    assert r.status_code in (200, 302)
