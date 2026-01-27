from pathlib import Path
import shutil

from fastapi import UploadFile, HTTPException

from .config import MAX_FILE_SIZE_MB, RASTER_EXT, VECTOR_EXT


def validate_file(file: UploadFile):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in RASTER_EXT + VECTOR_EXT:
        raise HTTPException(status_code=400, detail="Unsupported file format")


def save_upload_file(upload_file: UploadFile, destination: Path):
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    size = 0

    with destination.open("wb") as buffer:
        while True:
            chunk = upload_file.file.read(1024 * 1024)  # 1 MB
            if not chunk:
                break
            size += len(chunk)
            if size > max_bytes:
                raise HTTPException(status_code=413, detail="File too large")
            buffer.write(chunk)


def prepare_multi_input(files, upload_dir: Path) -> Path:
    saved = []

    for f in files:
        out = upload_dir / f.filename
        save_upload_file(f, out)
        saved.append(out)

    # If single file → return file
    if len(saved) == 1:
        return saved[0]

    # If multiple → assume shapefile set
    return upload_dir


def is_raster(path: Path) -> bool:
    return path.suffix.lower() in RASTER_EXT