from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


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


def reproject_vector(src: Path, dst: Path, target_crs: str):
    gdf = gpd.read_file(src)
    gdf = gdf.to_crs(target_crs)
    gdf.to_file(dst)


def reproject_raster(src: Path, dst: Path, target_crs: str):
    with rasterio.open(src) as src_ds:
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
