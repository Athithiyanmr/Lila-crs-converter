from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List
import uuid

from .config import APP_NAME, VERSION, UPLOAD_DIR, OUTPUT_DIR
from .utils import validate_file, is_raster, prepare_multi_input
from .crs import detect_crs, reproject_raster, reproject_vector

app = FastAPI(title=APP_NAME, version=VERSION)


@app.get("/")
def home():
    return {"status": "GeoCRS Converter API running"}


@app.post("/detect-crs")
async def detect(files: List[UploadFile] = File(...)):
    try:
        for f in files:
            validate_file(f)

        in_path = prepare_multi_input(files, UPLOAD_DIR)
        crs = detect_crs(in_path)

        return {"crs": crs}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/convert")
async def convert(
    files: List[UploadFile] = File(...),
    target_crs: str = Form(...)
):
    try:
        for f in files:
            validate_file(f)

        uid = uuid.uuid4().hex
        in_path = prepare_multi_input(files, UPLOAD_DIR)

        if is_raster(in_path):
            out_path = OUTPUT_DIR / f"reprojected_{uid}.tif"
            reproject_raster(in_path, out_path, target_crs)
        else:
            out_path = OUTPUT_DIR / f"reprojected_{uid}.geojson"
            reproject_vector(in_path, out_path, target_crs)

        return FileResponse(out_path, filename=out_path.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))