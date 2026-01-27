import sys
from pathlib import Path
from unittest.mock import MagicMock

# =================================
# MOCK HEAVY GIS DEPENDENCIES
# =================================

mock = MagicMock()

# rasterio and submodules
sys.modules["rasterio"] = mock
sys.modules["rasterio.warp"] = mock
sys.modules["rasterio.enums"] = mock
sys.modules["rasterio.crs"] = mock

# geopandas and stack
sys.modules["geopandas"] = mock
sys.modules["fiona"] = mock
sys.modules["pyproj"] = mock
sys.modules["shapely"] = mock
sys.modules["shapely.geometry"] = mock

# =================================
# Add project root to PYTHONPATH
# =================================

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_docs():
    r = client.get("/docs")
    assert r.status_code in (200, 302)
