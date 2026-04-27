import streamlit as st
import requests

# =========================
# CONFIG
# =========================

API = "http://geocrs-api:8000"
st.set_page_config(
    page_title="Lila CRS Converter",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Global font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Hide default Streamlit header/footer/menu */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 860px !important; }

/* ---- HERO BANNER ---- */
.lila-hero {
    background: linear-gradient(135deg, #f7f6f2 0%, #f0fafa 60%, #d2dedd 100%);
    border: 1px solid #dbd5cc;
    border-radius: 14px;
    padding: 2rem 2.25rem 1.75rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.lila-hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(1,105,111,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.lila-hero-eyebrow {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #01696f; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 6px;
}
.lila-hero-eyebrow::before { content:''; width:14px; height:2px; background:#01696f; border-radius:1px; display:inline-block; }
.lila-hero h1 {
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    font-weight: 700; letter-spacing: -0.025em;
    line-height: 1.1; color: #1c1a16; margin: 0 0 0.6rem;
}
.lila-hero h1 em { font-style: normal; color: #01696f; }
.lila-hero p { font-size: 0.88rem; color: #6d6560; max-width: 46ch; line-height: 1.75; margin: 0; }
.lila-fmt-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 1rem; }
.lila-chip {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 3px 10px; border-radius: 999px;
    background: #d2dedd; color: #01696f;
    border: 1px solid rgba(1,105,111,0.22);
}
.lila-chip.grey { background: #f0ede8; color: #6d6560; border-color: #dbd5cc; }

/* ---- STEP HEADER ---- */
.lila-step {
    display: flex; align-items: center; gap: 10px;
    margin: 1.5rem 0 0.75rem;
}
.lila-step-num {
    width: 20px; height: 20px; border-radius: 50%;
    background: #d2dedd; border: 1px solid rgba(1,105,111,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.55rem; font-weight: 800; color: #01696f; flex-shrink: 0;
}
.lila-step-label {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #01696f;
}
.lila-step-line { flex: 1; height: 1px; background: #e5e0d8; }

/* ---- METRIC CARDS ---- */
.lila-metrics { display: flex; gap: 10px; flex-wrap: wrap; margin: 0.75rem 0; }
.lila-metric {
    background: #f0ede8; border: 1px solid #dbd5cc;
    border-radius: 8px; padding: 10px 14px; min-width: 110px;
}
.lila-metric-label {
    font-size: 0.55rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #aaa49d; margin-bottom: 3px;
}
.lila-metric-value {
    font-size: 0.82rem; font-weight: 700; color: #1c1a16;
    font-family: 'JetBrains Mono', monospace;
}
.lila-metric-value.teal { color: #01696f; }

/* ---- CRS DETECTED BADGE ---- */
.lila-crs-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(1,105,111,0.07);
    border: 1px solid rgba(1,105,111,0.22);
    border-radius: 8px; padding: 8px 14px;
    font-size: 0.78rem; color: #6d6560; margin: 0.5rem 0;
}
.lila-crs-badge strong {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; color: #01696f;
}

/* ---- INFO BOX ---- */
.lila-info {
    background: rgba(1,105,111,0.06);
    border: 1px solid rgba(1,105,111,0.2);
    border-radius: 8px; padding: 9px 13px;
    font-size: 0.78rem; color: #01696f;
    margin-bottom: 1rem; line-height: 1.65;
}

/* ---- HISTORY TABLE ---- */
.lila-history-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 0.7fr 0.5fr;
    gap: 0; border-bottom: 1px solid #e5e0d8;
    font-size: 0.76rem;
}
.lila-history-row:last-child { border-bottom: none; }
.lila-th { font-size: 0.55rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #aaa49d; padding: 8px 10px; background: #f0ede8; }
.lila-td { padding: 9px 10px; color: #1c1a16; vertical-align: middle; }
.lila-tag-crs {
    font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    font-weight: 700; background: #d2dedd; color: #01696f;
    padding: 2px 7px; border-radius: 4px;
}
.lila-tag-fmt {
    font-size: 0.6rem; background: #f0ede8; color: #6d6560;
    padding: 2px 7px; border-radius: 4px; text-transform: uppercase;
    letter-spacing: 0.07em; font-weight: 600; border: 1px solid #dbd5cc;
}
.lila-tag-done { font-size: 0.68rem; color: #437a22; font-weight: 700; }

/* ---- FOOTER ---- */
.lila-footer {
    border-top: 1px solid #e5e0d8; margin-top: 2rem;
    padding-top: 1rem; display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 8px;
}
.lila-footer-left { font-size: 0.68rem; color: #aaa49d; }
.lila-footer-links { display: flex; gap: 16px; }
.lila-footer-links a {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #aaa49d; text-decoration: none;
}
.lila-footer-links a:hover { color: #01696f; }

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stFileUploader"] label {
    font-size: 0.6rem !important; font-weight: 700 !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    color: #6d6560 !important;
}
div[data-testid="stButton"] button {
    background: #01696f !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    padding: 0.45rem 1.1rem !important;
    box-shadow: 0 2px 6px rgba(1,105,111,0.25) !important;
    transition: background 0.18s ease !important;
}
div[data-testid="stButton"] button:hover {
    background: #0c4e54 !important;
}
div[data-testid="stButton"] button:disabled {
    background: #d2dedd !important; color: #aaa49d !important;
    box-shadow: none !important;
}
div[data-testid="stDownloadButton"] button {
    background: #d2dedd !important; color: #01696f !important;
    border: 1px solid rgba(1,105,111,0.22) !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown("""
<div class="lila-hero">
  <div class="lila-hero-eyebrow">Coordinate Reprojection</div>
  <h1>Reproject <em>Spatial Data</em> with Precision</h1>
  <p>Upload GeoTIFF, GeoJSON, or Shapefiles and instantly convert to any coordinate reference system.</p>
  <div class="lila-fmt-row">
    <span class="lila-chip">GeoTIFF</span>
    <span class="lila-chip">GeoJSON</span>
    <span class="lila-chip">Shapefile</span>
    <span class="lila-chip grey">GeoPackage out</span>
    <span class="lila-chip grey">Any EPSG</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# STEP 1 — UPLOAD
# =========================

st.markdown("""
<div class="lila-step">
  <div class="lila-step-num">1</div>
  <div class="lila-step-label">Upload Files</div>
  <div class="lila-step-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="lila-info">
  📌 For Shapefiles, upload <strong>all four parts together</strong>: .shp &nbsp;·&nbsp; .shx &nbsp;·&nbsp; .dbf &nbsp;·&nbsp; .prj
</div>
""", unsafe_allow_html=True)

files = st.file_uploader(
    "Upload GeoTIFF / GeoJSON / Shapefile set",
    type=["tif", "tiff", "geojson", "shp", "shx", "dbf", "prj"],
    accept_multiple_files=True,
    label_visibility="visible"
)

if files:
    total_mb = sum(f.size for f in files) / (1024 * 1024)
    names = ", ".join(f.name for f in files)
    st.markdown(f"""
    <div class="lila-metrics">
      <div class="lila-metric">
        <div class="lila-metric-label">Files</div>
        <div class="lila-metric-value">{len(files)}</div>
      </div>
      <div class="lila-metric">
        <div class="lila-metric-label">Total Size</div>
        <div class="lila-metric-value">{total_mb:.1f} MB</div>
      </div>
      <div class="lila-metric">
        <div class="lila-metric-label">Types</div>
        <div class="lila-metric-value">{", ".join(sorted(set(f.name.split(".")[-1].upper() for f in files)))}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if total_mb > 200:
        st.warning(f"⚠️ **{total_mb:.1f} MB** total — large files may take several minutes to convert.")

# =========================
# STEP 2 — CONFIGURE
# =========================

st.markdown("""
<div class="lila-step">
  <div class="lila-step-num">2</div>
  <div class="lila-step-label">Detect &amp; Configure CRS</div>
  <div class="lila-step-line"></div>
</div>
""", unsafe_allow_html=True)

if files:
    col_detect, col_spacer = st.columns([1, 3])
    with col_detect:
        if st.button("🔍 Detect Source CRS"):
            try:
                with st.spinner("Detecting CRS…"):
                    res = requests.post(
                        f"{API}/detect-crs",
                        files=[("files", f) for f in files],
                        timeout=300
                    )
                if res.status_code == 200:
                    detected = res.json().get("crs", "Unknown")
                    st.session_state["detected_crs"] = detected
                    st.success(f"Detected: **{detected}**")
                else:
                    st.error(res.json().get("detail", res.text))
            except Exception as e:
                st.error(f"Server error: {e}")

    if st.session_state.get("detected_crs"):
        st.markdown(f"""
        <div class="lila-crs-badge">
          🛡 Source CRS detected: &nbsp;<strong>{st.session_state["detected_crs"]}</strong>
        </div>
        """, unsafe_allow_html=True)

    col_crs, col_fmt = st.columns(2)

    PRESET_CRS = [
        "EPSG:4326  — WGS 84 (Lat/Lon)",
        "EPSG:3857  — Web Mercator",
        "EPSG:32643 — UTM Zone 43N",
        "EPSG:32644 — UTM Zone 44N",
        "EPSG:32645 — UTM Zone 45N",
        "EPSG:32646 — UTM Zone 46N",
        "EPSG:7755  — India NSF LCC (WGS84)",
        "EPSG:24378 — Kalianpur 1937 / India I",
        "EPSG:24379 — Kalianpur 1937 / India II",
        "EPSG:24380 — Kalianpur 1937 / India III",
        "EPSG:32642 — UTM Zone 42N",
        "EPSG:32647 — UTM Zone 47N",
        "Custom (enter below)",
    ]

    with col_crs:
        preset = st.selectbox("Target CRS", PRESET_CRS)
        if preset == "Custom (enter below)":
            custom_epsg = st.text_input(
                "Custom EPSG code",
                placeholder="e.g. EPSG:7760",
                help="Find any EPSG code at epsg.io"
            )
            target_crs = custom_epsg.strip().upper() if custom_epsg else ""
            if target_crs and not target_crs.startswith("EPSG:"):
                st.warning("⚠️ Must start with 'EPSG:' — e.g. EPSG:4326")
                target_crs = ""
        else:
            target_crs = preset.split()[0]

    with col_fmt:
        output_format_ui = st.selectbox(
            "Output Format",
            ["GeoJSON (.geojson)", "GeoPackage (.gpkg)", "Shapefile (.zip)"]
        )

    out_fmt = "geojson" if "GeoJSON" in output_format_ui else ("gpkg" if "GeoPackage" in output_format_ui else "shapefile")

else:
    st.caption("Upload files above to configure CRS options.")
    target_crs = ""
    out_fmt = "geojson"

# =========================
# STEP 3 — CONVERT
# =========================

st.markdown("""
<div class="lila-step">
  <div class="lila-step-num">3</div>
  <div class="lila-step-label">Convert &amp; Download</div>
  <div class="lila-step-line"></div>
</div>
""", unsafe_allow_html=True)

convert_ready = bool(files and target_crs)

if not files:
    st.caption("Upload files in Step 1 to enable conversion.")
elif not target_crs:
    st.caption("Select or enter a target CRS in Step 2 to enable conversion.")

if convert_ready:
    if st.button("♻️ Convert CRS", disabled=not convert_ready):
        try:
            with st.spinner("Reprojecting… this may take a moment for large files."):
                res = requests.post(
                    f"{API}/convert",
                    files=[("files", f) for f in files],
                    data={"target_crs": target_crs, "output_format": out_fmt},
                    timeout=1800
                )

            if res.status_code == 200:
                st.success("✅ Conversion complete!")

                if "history" not in st.session_state:
                    st.session_state["history"] = []
                st.session_state["history"].insert(0, {
                    "files": ", ".join(f.name for f in files),
                    "source": st.session_state.get("detected_crs", "—"),
                    "target": target_crs,
                    "format": out_fmt,
                })

                ext_map = {"geojson": "reprojected.geojson", "gpkg": "reprojected.gpkg", "shapefile": "reprojected.zip"}
                out_name = "reprojected.tif" if any(f.name.lower().endswith((".tif", ".tiff")) for f in files) else ext_map[out_fmt]

                st.download_button(
                    "⬇️ Download Converted File",
                    data=res.content,
                    file_name=out_name,
                    mime="application/octet-stream"
                )
            else:
                st.error(res.json().get("detail", res.text))

        except Exception as e:
            st.error(f"Server error: {e}")

# =========================
# SESSION HISTORY
# =========================

if st.session_state.get("history"):
    st.markdown("""
    <div class="lila-step" style="margin-top:1.5rem;">
      <div class="lila-step-num" style="background:#f0ede8;color:#aaa49d;border-color:#dbd5cc;">↺</div>
      <div class="lila-step-label">Session History</div>
      <div class="lila-step-line"></div>
    </div>
    """, unsafe_allow_html=True)

    rows_html = ""
    for h in st.session_state["history"]:
        rows_html += f"""
        <div class="lila-history-row">
          <div class="lila-td" style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{h['files']}</div>
          <div class="lila-td"><span class="lila-tag-crs" style="opacity:.7">{h['source']}</span></div>
          <div class="lila-td"><span class="lila-tag-crs">{h['target']}</span></div>
          <div class="lila-td"><span class="lila-tag-fmt">{h['format']}</span></div>
          <div class="lila-td"><span class="lila-tag-done">✓ Done</span></div>
        </div>
        """

    st.markdown(f"""
    <div style="border:1px solid #e5e0d8;border-radius:10px;overflow:hidden;margin-top:0.5rem;">
      <div class="lila-history-row">
        <div class="lila-th">Files</div>
        <div class="lila-th">Source CRS</div>
        <div class="lila-th">Target CRS</div>
        <div class="lila-th">Format</div>
        <div class="lila-th">Status</div>
      </div>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown("""
<div class="lila-footer">
  <div class="lila-footer-left">Built by <strong>Athithiyan MR</strong> — Lila Geospatial Platform</div>
  <div class="lila-footer-links">
    <a href="https://epsg.io" target="_blank">EPSG.io</a>
    <a href="https://proj.org" target="_blank">PROJ Docs</a>
    <a href="https://github.com/Athithiyanmr/Lila-crs-converter" target="_blank">GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)
