import streamlit as st
import requests

# =========================
# CONFIG
# =========================

API = "http://backend:8000"
st.set_page_config(page_title="Lila CRS Converter", layout="centered")
st.set_option("server.maxUploadSize", 1024)  # 1 GB

# =========================
# UI
# =========================

st.title("🌍 Lila CRS Converter")
st.caption("Simple, reliable CRS conversion for geospatial data")

st.info("ℹ️ For shapefiles, upload ALL parts together (.shp, .shx, .dbf, .prj).")

# =========================
# Upload
# =========================

files = st.file_uploader(
    "Upload GeoTIFF / GeoJSON or Shapefile set",
    type=["tif", "tiff", "geojson", "shp", "shx", "dbf", "prj"],
    accept_multiple_files=True
)

if files:
    st.success(f"{len(files)} file(s) selected")

# =========================
# Main logic
# =========================

if files and len(files) > 0:

    col1, col2 = st.columns(2)

    # -------- Detect CRS --------
    with col1:
        if st.button("🔍 Detect CRS"):
            try:
                with st.spinner("Detecting CRS..."):
                    multipart_files = [("files", f) for f in files]

                    res = requests.post(
                        f"{API}/detect-crs",
                        files=multipart_files,
                        timeout=300
                    )

                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Detected CRS: {data.get('crs', 'Unknown')}")
                else:
                    st.error(res.json().get("detail", res.text))

            except Exception as e:
                st.error(f"Server error: {e}")

    # -------- CRS selection --------
    with col2:
        target = st.selectbox(
            "Select target CRS",
            [
                "EPSG:4326  (WGS84 Lat/Lon)",
                "EPSG:3857  (Web Mercator)",
                "EPSG:32643 (UTM Zone 43N)",
                "EPSG:32644 (UTM Zone 44N)",
                "EPSG:32645 (UTM Zone 45N)"
            ]
        )

    target_crs = target.split()[0]

    # -------- Convert CRS --------
    if st.button("♻️ Convert CRS"):
        try:
            with st.spinner("Reprojecting data... This may take some time."):

                multipart_files = [("files", f) for f in files]

                res = requests.post(
                    f"{API}/convert",
                    files=multipart_files,
                    data={"target_crs": target_crs},
                    timeout=1800
                )

            if res.status_code == 200:
                st.success("✅ Conversion successful!")

                if any(f.name.lower().endswith((".tif", ".tiff")) for f in files):
                    out_name = "reprojected.tif"
                else:
                    out_name = "reprojected.geojson"

                st.download_button(
                    "⬇ Download converted file",
                    data=res.content,
                    file_name=out_name,
                    mime="application/octet-stream"
                )

            else:
                st.error(res.json().get("detail", res.text))

        except Exception as e:
            st.error(f"Server error: {e}")

# =========================
# Footer
# =========================

st.markdown("---")
st.caption("Built by Athithiyan MR | Lila Geospatial Platform")