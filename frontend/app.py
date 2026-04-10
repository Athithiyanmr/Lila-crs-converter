import streamlit as st
import requests

# =========================
# CONFIG
# =========================

API = "http://geocrs-api:8000"
st.set_page_config(page_title="Lila CRS Converter", layout="centered")

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
                    detected = data.get('crs', 'Unknown')
                    st.success(f"Detected CRS: **{detected}**")
                    st.session_state["detected_crs"] = detected
                else:
                    st.error(res.json().get("detail", res.text))

            except Exception as e:
                st.error(f"Server error: {e}")

    # -------- CRS & OUTPUT FORMAT --------
    with col2:
        # Preset CRS dropdown
        PRESET_CRS = [
            "Custom (enter below)",
            "EPSG:4326  (WGS84 Lat/Lon)",
            "EPSG:3857  (Web Mercator)",
            "EPSG:32643 (UTM Zone 43N)",
            "EPSG:32644 (UTM Zone 44N)",
            "EPSG:32645 (UTM Zone 45N)",
            "EPSG:32646 (UTM Zone 46N)",
            "EPSG:7755  (India WGS84 / India NSF LCC)",
            "EPSG:24378 (Kalianpur 1962 / India Zone I)",
        ]

        preset = st.selectbox("Select target CRS", PRESET_CRS)

        # Show custom text input only when "Custom" is selected
        if preset == "Custom (enter below)":
            custom_epsg = st.text_input(
                "Enter custom EPSG code",
                placeholder="e.g. EPSG:7760 or EPSG:32644",
                help="Enter any valid EPSG code. Find codes at epsg.io"
            )
            target_crs = custom_epsg.strip().upper() if custom_epsg else ""
            if target_crs and not target_crs.startswith("EPSG:"):
                st.warning("⚠️ EPSG code should start with 'EPSG:' — e.g. EPSG:4326")
                target_crs = ""
        else:
            target_crs = preset.split()[0]  # Extract just the EPSG code

        output_format_ui = st.selectbox(
            "Select output format (for vector data)",
            [
                "GeoJSON (.geojson)",
                "GeoPackage (.gpkg)",
                "Shapefile (.zip)"
            ]
        )

    if "GeoJSON" in output_format_ui:
        out_fmt = "geojson"
    elif "GeoPackage" in output_format_ui:
        out_fmt = "gpkg"
    else:
        out_fmt = "shapefile"

    # -------- File size warning --------
    total_size_mb = sum(f.size for f in files) / (1024 * 1024)
    if total_size_mb > 200:
        st.warning(
            f"⚠️ Total upload size is **{total_size_mb:.1f} MB**. "
            "Large files may take several minutes to convert."
        )

    # -------- Convert CRS --------
    convert_ready = target_crs != ""
    if not convert_ready and preset == "Custom (enter below)":
        st.caption("Enter a valid EPSG code above to enable conversion.")

    if st.button("♻️ Convert CRS", disabled=not convert_ready):
        try:
            with st.spinner("Reprojecting data... This may take some time."):

                multipart_files = [("files", f) for f in files]

                res = requests.post(
                    f"{API}/convert",
                    files=multipart_files,
                    data={
                        "target_crs": target_crs,
                        "output_format": out_fmt
                    },
                    timeout=1800
                )

            if res.status_code == 200:
                st.success("✅ Conversion successful!")

                # Log to session history
                if "history" not in st.session_state:
                    st.session_state["history"] = []
                st.session_state["history"].append({
                    "Files": ", ".join(f.name for f in files),
                    "Target CRS": target_crs,
                    "Format": out_fmt
                })

                # Output filename
                if any(f.name.lower().endswith((".tif", ".tiff")) for f in files):
                    out_name = "reprojected.tif"
                else:
                    if out_fmt == "geojson":
                        out_name = "reprojected.geojson"
                    elif out_fmt == "gpkg":
                        out_name = "reprojected.gpkg"
                    else:
                        out_name = "reprojected.zip"

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
# Conversion History
# =========================

if st.session_state.get("history"):
    st.markdown("---")
    st.subheader("📋 Session Conversion History")
    st.dataframe(
        st.session_state["history"],
        use_container_width=True,
        hide_index=True
    )

# =========================
# Footer
# =========================

st.markdown("---")
st.caption("Built by Athithiyan MR | Lila Geospatial Platform")
