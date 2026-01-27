from pathlib import Path

APP_NAME = "GeoCRS Converter"
VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

RASTER_EXT = [".tif", ".tiff"]
VECTOR_EXT = [".geojson", ".gpkg", ".shp", ".shx", ".dbf", ".prj"]

MAX_FILE_SIZE_MB = 500