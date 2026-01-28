from pathlib import Path
import shutil
import zipfile

import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


# =====================================================
# CRS DETECTION
# =====================================================

def detect_crs(file_path: Path) -> str:
    if file_path.suffix.lower() in [".tif", ".tiff"]:
        with rasterio.open(file_path) as ds:
            if ds.crs is None:
                raise ValueError("Raster has no CRS defined")
            return ds.crs.to_string()
    else:
        gdf = gpd.read_file(file_path)
        if gdf.crs is None:
            raise ValueError("Vector has no CRS defined")
        return gdf.crs.to_string()


# =====================================================
# VECTOR REPROJECTION (GeoJSON / GPKG / Shapefile ZIP)
# =====================================================

def reproject_vector(
    src: Path,
    out_base: Path,
    target_crs: str,
    output_format: str = "geojson"
) -> Path:

    gdf = gpd.read_file(src)

    if gdf.crs is None:
        raise ValueError("Vector has no CRS defined")

    gdf = gdf.to_crs(target_crs)

    output_format = output_format.lower()

    if output_format == "geojson":
        out_path = out_base.with_suffix(".geojson")
        gdf.to_file(out_path, driver="GeoJSON")
        return out_path

    elif output_format == "gpkg":
        out_path = out_base.with_suffix(".gpkg")
        gdf.to_file(out_path, driver="GPKG")
        return out_path

    elif output_format in ["shp", "shapefile"]:
        shp_dir = out_base.parent / out_base.stem
        shp_dir.mkdir(parents=True, exist_ok=True)

        shp_path = shp_dir / f"{out_base.stem}.shp"
        gdf.to_file(shp_path, driver="ESRI Shapefile")

        zip_path = out_base.with_suffix(".zip")
        zip_shapefile(shp_dir, zip_path)

        shutil.rmtree(shp_dir)
        return zip_path

    else:
        raise ValueError("Unsupported output format. Use: geojson, gpkg, shapefile")


# =====================================================
# RASTER REPROJECTION (GeoTIFF)
# =====================================================

def reproject_raster(src: Path, dst: Path, target_crs: str) -> Path:

    with rasterio.open(src) as src_ds:

        if src_ds.crs is None:
            raise ValueError("Raster has no CRS defined")

        transform, width, height = calculate_default_transform(
            src_ds.crs, target_crs,
            src_ds.width, src_ds.height,
            *src_ds.bounds
        )

        meta = src_ds.meta.copy()
        meta.update({
            "crs": target_crs,
            "transform": transform,
            "width": width,
            "height": height
        })

        with rasterio.open(dst, "w", **meta) as dst_ds:
            for i in range(1, src_ds.count + 1):
                reproject(
                    source=rasterio.band(src_ds, i),
                    destination=rasterio.band(dst_ds, i),
                    src_transform=src_ds.transform,
                    src_crs=src_ds.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest
                )

    return dst


# =====================================================
# SHAPEFILE ZIP HELPER
# =====================================================

def zip_shapefile(folder: Path, zip_path: Path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in folder.iterdir():
            zipf.write(file, file.name)
