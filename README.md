🌍 Lila CRS Converter

Lila CRS Converter is a containerized geospatial web platform for detecting and converting Coordinate Reference Systems (CRS) of raster and vector datasets.

It is designed for GIS analysts, remote sensing engineers, and geospatial developers who need a fast, reliable way to reproject data directly in the browser.

⸻

✨ What you can do

With Lila CRS Converter, you can:
	•	Upload raster or vector geospatial data
	•	Automatically detect the existing CRS
	•	Select a target EPSG coordinate system
	•	Reproject the dataset
	•	Download the converted output

Supported formats:
	•	🛰️ GeoTIFF (raster)
	•	🗺️ Shapefile (multi-file upload)
	•	🧩 GeoJSON, GeoPackage (vector)

⸻

🚀 Features
	•	✅ Raster reprojection (GeoTIFF)
	•	✅ Vector reprojection (Shapefile, GeoJSON, GPKG)
	•	✅ Multi-file shapefile upload support
	•	✅ Automatic CRS detection
	•	✅ FastAPI backend (high-performance API)
	•	✅ Streamlit frontend (interactive web UI)
	•	✅ Fully Dockerized architecture
	•	✅ Cloud-ready deployment
	•	✅ Designed as a base for future GeoAI & NDVI tools

⸻

🏗️ Project Structure


lila-crs-converter/
│
├── backend/
│   ├── main.py          # FastAPI application
│   ├── crs.py           # CRS detection & reprojection logic
│   ├── utils.py         # File handling & validation
│   ├── config.py        # App configuration
│
├── frontend/
│   └── app.py           # Streamlit web interface
│
├── docker-compose.yml   # Multi-container setup
├── Dockerfile           # Backend container
└── README.md



⚙️ How it works
	1.	Frontend (Streamlit) handles file upload and user interaction
	2.	Backend (FastAPI) processes CRS detection and reprojection
	3.	Raster data is returned as GeoTIFF
	4.	Vector data is exported as a shapefile and delivered as a ZIP
	5.	Everything runs in isolated Docker containers
  
🐳 Run locally

git clone https://github.com/your-username/geo-crs-converter.git
cd geo-crs-converter
docker compose up --build

then run:
http://localhost:8501

☁️ Deployment

This project is designed for cloud deployment using Docker.

🚧 Hetzner cloud deployment is in progress.
A public website link will be added here soon.

Once deployed, users will be able to access Lila CRS Converter directly from the browser without local installation.

👤 Author

Athithiyan MR
Data Analyst | Geospatial & Remote Sensing Specialist | GeoAI & Climate Analytics

ChatGPT-5.2 

🔗 LinkedIn: https://www.linkedin.com/in/athithiyan-m-r-/
💻 GitHub: https://github.com/Athithiyanmr

## 📜 License
MIT License © 2026 Athithiyan MR
