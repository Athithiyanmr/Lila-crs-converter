# 🌍 Lila CRS Converter

> **A production-ready, containerized geospatial web platform for CRS detection and reprojection of raster and vector datasets — built with FastAPI, Streamlit, and Docker.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-crs.thelila.org-2E9E6B?style=flat-square&logo=globe&logoColor=white)](https://crs.thelila.org)

---

## 🔗 Live Demo

👉 **[crs.thelila.org](https://crs.thelila.org)** — Try it in your browser, no setup required.

---

## 📌 What Is This?

GIS analysts and remote sensing engineers frequently work with spatial datasets in mismatched or unknown coordinate systems. Reprojecting files traditionally requires desktop GIS software like QGIS or ArcGIS — which are heavy, slow, and unavailable in server or automated pipeline environments.

**Lila CRS Converter** solves this with a lightweight, browser-accessible platform where you can:

- Upload any raster or vector geospatial file
- Automatically detect its source CRS
- Select a target EPSG code
- Reproject and download the converted output — all in the browser

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Auto CRS Detection | Detects source coordinate system from uploaded file metadata |
| 🔄 Raster Reprojection | Reprojects GeoTIFF files to any EPSG code |
| 🗺️ Vector Reprojection | Reprojects Shapefiles (ZIP), GeoJSON, GeoPackage |
| 📦 Multi-file Shapefile | Upload `.shp`, `.dbf`, `.prj` together or as a ZIP |
| ⚡ High-performance API | FastAPI backend handles large files efficiently |
| 🐳 Fully Containerized | Docker + docker-compose for reproducible environments |
| ✅ CI Tested | GitHub Actions pipeline validates every push |
| 🔒 HTTPS Deployed | Secure HTTPS on a self-hosted VPS server |

---

## 🗂️ Supported Formats

- 🛰️ **Raster** — GeoTIFF (`.tif`, `.tiff`)
- 🗺️ **Vector** — Shapefile (`.zip`), GeoJSON (`.geojson`), GeoPackage (`.gpkg`)

---

## 🏗️ Architecture

```
lila-crs-converter/
│
├── backend/
│   ├── main.py          # FastAPI app & API routes
│   ├── crs.py           # CRS detection & reprojection engine
│   ├── utils.py         # File validation & temp handling
│   └── config.py        # App configuration
│
├── frontend/
│   └── app.py           # Streamlit web interface
│
├── tests/               # Unit & integration tests
├── .github/             # GitHub Actions CI workflows
├── docker-compose.yml   # Multi-container orchestration
├── Dockerfile           # Frontend container definition
└── requirements.txt
```

**How it works:**
1. Streamlit frontend handles file upload and user interaction
2. Uploaded file is sent to the FastAPI backend via REST API
3. Backend detects CRS using GDAL/pyproj and performs reprojection
4. Reprojected file is returned to the user for download
5. All services run in isolated Docker containers

---

## 🚀 Run Locally with Docker

```bash
git clone https://github.com/Athithiyanmr/Lila-crs-converter.git
cd Lila-crs-converter
docker compose up --build
```

Open in browser:
```
http://localhost:8501
```

---

## ⚙️ Run Without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend
uvicorn backend.main:app --reload --port 8000

# Start Streamlit frontend (new terminal)
streamlit run frontend/app.py
```

---

## 🧪 Testing

```bash
pytest tests/
```

CI runs automatically on every push via GitHub Actions.

---

## ☁️ Deployment

Deployed on a **self-hosted VPS** with:
- Docker containerization
- HTTPS via reverse proxy (Nginx + SSL)
- GitHub Actions CI for automated testing before deploy

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Geospatial Engine | GDAL, Rasterio, GeoPandas, pyproj |
| Containerization | Docker, docker-compose |
| CI/CD | GitHub Actions |
| Deployment | Self-hosted VPS, HTTPS |

---

## 🗺️ Roadmap

- [ ] NDVI and spectral index computation module
- [ ] Batch reprojection for multiple files
- [ ] GeoAI integration for automated spatial analysis
- [ ] REST API documentation (Swagger UI already built-in via FastAPI)

---

## 👤 Author

**Athithiyan M R** — Geospatial Data Scientist | Remote Sensing | Climate Analytics

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/athithiyan-m-r-/)
[![GitHub](https://img.shields.io/badge/GitHub-Athithiyanmr-181717?style=flat-square&logo=github)](https://github.com/Athithiyanmr)

---

## 📜 License

MIT License © 2026 Athithiyan M R
