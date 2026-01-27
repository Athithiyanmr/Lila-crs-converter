FROM condaforge/mambaforge:24.1.2-0

WORKDIR /app

# install dependencies
RUN mamba install -y -c conda-forge \
    python=3.10 \
    fastapi \
    uvicorn \
    rasterio \
    geopandas \
    shapely

# copy full backend package
COPY backend /app/backend

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]