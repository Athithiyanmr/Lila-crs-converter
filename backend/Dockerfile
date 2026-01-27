FROM condaforge/mambaforge:24.1.2-0

WORKDIR /app

# Install geospatial stack safely from conda-forge
RUN mamba install -y -c conda-forge \
    python=3.10 \
    fastapi \
    uvicorn \
    rasterio \
    geopandas \
    shapely \
    fiona \
    pyproj \
    numpy \
    requests \
    python-multipart \
    matplotlib \
    pillow \
 && mamba clean -a -y

COPY app/ /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]