from pathlib import Path

APP_NAME = "GeoCRS Converter"
VERSION = "1.0.0"

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RASTER_EXT = [".tif", ".tiff"]
VECTOR_EXT = [".geojson", ".gpkg", ".shp", ".shx", ".dbf", ".prj"]

MAX_FILE_SIZE_MB = 1024  # 1 GB