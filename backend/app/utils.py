from pathlib import Path
from fastapi import UploadFile, HTTPException
from config import RASTER_EXT, VECTOR_EXT, MAX_FILE_SIZE_MB


def save_upload(upload: UploadFile, out_path: Path):
    with open(out_path, "wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def validate_file(file: UploadFile):

    suffix = Path(file.filename).suffix.lower()

    if suffix not in RASTER_EXT + VECTOR_EXT:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload GeoTIFF, SHP, GeoJSON or GPKG."
        )

    return suffix


def is_raster(path: Path) -> bool:
    return path.suffix.lower() in RASTER_EXT


def is_vector(path: Path) -> bool:
    return path.suffix.lower() in VECTOR_EXT
