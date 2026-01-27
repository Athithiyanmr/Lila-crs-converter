from pathlib import Path
import uuid, shutil

# Allowed single-file formats + shapefile parts
ALLOWED = (".tif", ".tiff", ".geojson", ".shp", ".shx", ".dbf", ".prj")


# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate_file(file):
    if not file.filename.lower().endswith(ALLOWED):
        raise ValueError(f"Unsupported file type: {file.filename}")


# --------------------------------------------------
# Raster check
# --------------------------------------------------

def is_raster(path: Path):
    return path.suffix.lower() in (".tif", ".tiff")


# --------------------------------------------------
# Multi-file input handler (KEY FIX)
# --------------------------------------------------

def prepare_multi_input(files, upload_dir: Path):

    uid = uuid.uuid4().hex
    work_dir = upload_dir / uid
    work_dir.mkdir(parents=True, exist_ok=True)

    saved = []

    # Save all uploaded files into one folder
    for f in files:
        out = work_dir / f.filename
        with open(out, "wb") as buf:
            shutil.copyfileobj(f.file, buf)
        saved.append(out)

    # Case 1: Single file (GeoTIFF / GeoJSON)
    if len(saved) == 1:
        return saved[0]

    # Case 2: Multiple files → assume shapefile set
    shp_files = list(work_dir.glob("*.shp"))

    if not shp_files:
        raise ValueError("No .shp file found. Upload all shapefile parts together.")

    # Return the .shp path (GeoPandas will read .shx/.dbf/.prj automatically)
    return shp_files[0]