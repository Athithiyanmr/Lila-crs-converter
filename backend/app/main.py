from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid

from config import APP_NAME, VERSION, UPLOAD_DIR, OUTPUT_DIR
from utils import save_upload, validate_file, is_raster
from crs import detect_crs, reproject_raster, reproject_vector

app = FastAPI(title=APP_NAME, version=VERSION)


@app.post("/detect-crs")
async def detect(file: UploadFile = File(...)):

    validate_file(file)

    in_path = UPLOAD_DIR / f"{uuid.uuid4().hex}_{file.filename}"
    save_upload(file, in_path)

    crs = detect_crs(in_path)
    return {"filename": file.filename, "crs": crs}


@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    target_crs: str = Form(...)
):

    validate_file(file)

    uid = uuid.uuid4().hex
    in_path = UPLOAD_DIR / f"{uid}_{file.filename}"
    out_path = OUTPUT_DIR / f"reprojected_{file.filename}"

    save_upload(file, in_path)

    try:
        if is_raster(in_path):
            reproject_raster(in_path, out_path, target_crs)
        else:
            reproject_vector(in_path, out_path, target_crs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return FileResponse(out_path, filename=out_path.name)
