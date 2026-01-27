import streamlit as st
import requests

API = "http://backend:8000"

st.set_page_config(page_title="GeoCRS Converter", layout="centered")
st.title("🌍 GeoCRS – Coordinate System Converter")

file = st.file_uploader("Upload raster (GeoTIFF) or vector (GeoJSON / SHP zip)")

if file:
    if st.button("Detect CRS"):
        res = requests.post(f"{API}/detect-crs", files={"file": file})
        data = res.json()
        st.success(f"Detected CRS: {data['crs']}")

    target = st.selectbox(
        "Select target CRS",
        ["EPSG:4326", "EPSG:3857", "EPSG:32643", "EPSG:32644", "EPSG:32645"]
    )

    if st.button("Convert CRS"):
        res = requests.post(
            f"{API}/convert",
            files={"file": file},
            data={"target_crs": target}
        )

        st.download_button(
            "⬇ Download converted file",
            data=res.content,
            file_name="converted_" + file.name
        )
