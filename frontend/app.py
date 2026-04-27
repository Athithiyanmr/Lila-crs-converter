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
    initial_sidebar_state="expanded"
)

# =========================
# EPSG LOOKUP TABLE
# =========================

EPSG_NAMES = {
    "EPSG:4326":  "WGS 84 — Geographic (Lat/Lon)",
    "EPSG:3857":  "Web Mercator (Google Maps)",
    "EPSG:32638": "WGS 84 / UTM Zone 38N",
    "EPSG:32639": "WGS 84 / UTM Zone 39N",
    "EPSG:32640": "WGS 84 / UTM Zone 40N",
    "EPSG:32641": "WGS 84 / UTM Zone 41N",
    "EPSG:32642": "WGS 84 / UTM Zone 42N",
    "EPSG:32643": "WGS 84 / UTM Zone 43N",
    "EPSG:32644": "WGS 84 / UTM Zone 44N",
    "EPSG:32645": "WGS 84 / UTM Zone 45N",
    "EPSG:32646": "WGS 84 / UTM Zone 46N",
    "EPSG:32647": "WGS 84 / UTM Zone 47N",
    "EPSG:7755":  "WGS 84 / India NSF LCC",
    "EPSG:7756":  "WGS 84 / India NE",
    "EPSG:7757":  "WGS 84 / India NW",
    "EPSG:7758":  "WGS 84 / India SE",
    "EPSG:7759":  "WGS 84 / India SW",
    "EPSG:7760":  "WGS 84 / India NE (alt)",
    "EPSG:24378": "Kalianpur 1937 / India Zone I",
    "EPSG:24379": "Kalianpur 1937 / India Zone II",
    "EPSG:24380": "Kalianpur 1937 / India Zone III",
    "EPSG:24381": "Kalianpur 1937 / India Zone IV",
    "EPSG:900913":"Google Mercator (deprecated)",
    "EPSG:4269":  "NAD83 — North America",
    "EPSG:4258":  "ETRS89 — Europe",
    "EPSG:27700": "British National Grid",
    "EPSG:2154":  "RGF93 / Lambert-93 (France)",
    "EPSG:25832": "ETRS89 / UTM Zone 32N (Europe)",
}

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

# =========================
# SESSION STATE DEFAULTS
# =========================

for key, val in [("dark", False), ("detected_crs", None), ("history", []), ("converted", False), ("target_crs_final", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

# =========================
# THEME COLORS
# =========================

if st.session_state.dark:
    BG         = "#171614"
    SURFACE    = "#1c1b19"
    SURFACE2   = "#22211f"
    BORDER     = "#393836"
    TEXT       = "#cdccca"
    MUTED      = "#797876"
    FAINT      = "#5a5957"
    PRIMARY    = "#4f98a3"
    PRIMARY_BG = "rgba(79,152,163,0.12)"
    PRIMARY_BR = "rgba(79,152,163,0.28)"
    SHADOW     = "0 4px 16px rgba(0,0,0,0.35)"
    HERO_GRAD  = "linear-gradient(135deg,#1a2424 0%,#1c2b2b 60%,#1f3333 100%)"
    BTN_BG     = "#4f98a3"
    BTN_HOVER  = "#227f8b"
    CHIP_BG    = "#313b3b"
    CHIP_COLOR = "#4f98a3"
    METRIC_BG  = "#22211f"
    INFO_BG    = "rgba(79,152,163,0.08)"
    HIST_HEAD  = "#22211f"
    TAG_BG     = "#313b3b"
    SUCCESS    = "#6daa45"
else:
    BG         = "#f7f6f2"
    SURFACE    = "#ffffff"
    SURFACE2   = "#f0ede8"
    BORDER     = "#dbd5cc"
    TEXT       = "#1c1a16"
    MUTED      = "#6d6560"
    FAINT      = "#aaa49d"
    PRIMARY    = "#01696f"
    PRIMARY_BG = "rgba(1,105,111,0.07)"
    PRIMARY_BR = "rgba(1,105,111,0.22)"
    SHADOW     = "0 4px 16px rgba(28,26,22,0.10)"
    HERO_GRAD  = "linear-gradient(135deg,#f7f6f2 0%,#edf6f6 60%,#d2dedd 100%)"
    BTN_BG     = "#01696f"
    BTN_HOVER  = "#0c4e54"
    CHIP_BG    = "#d2dedd"
    CHIP_COLOR = "#01696f"
    METRIC_BG  = "#f0ede8"
    INFO_BG    = "rgba(1,105,111,0.06)"
    HIST_HEAD  = "#f0ede8"
    TAG_BG     = "#d2dedd"
    SUCCESS    = "#437a22"

# =========================
# CUSTOM CSS
# =========================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    min-width: 270px !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

/* HERO */
.lila-hero {{
    background: {HERO_GRAD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 2.25rem 2.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: {SHADOW};
}}
.lila-hero::before {{
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, {PRIMARY_BG} 0%, transparent 70%);
    pointer-events: none;
    animation: pulse 4s ease-in-out infinite;
}}
.lila-hero::after {{
    content: '';
    position: absolute; bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, {PRIMARY_BG} 0%, transparent 70%);
    pointer-events: none;
    animation: pulse 4s ease-in-out infinite 2s;
}}
@keyframes pulse {{
    0%,100% {{ opacity:0.5; transform:scale(1); }}
    50% {{ opacity:1; transform:scale(1.15); }}
}}
.lila-eyebrow {{
    font-size: 0.58rem; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: {PRIMARY};
    display: flex; align-items: center; gap: 8px; margin-bottom: 0.6rem;
}}
.lila-eyebrow span {{ width:18px; height:2px; background:{PRIMARY}; border-radius:1px; display:inline-block; }}
.lila-hero h1 {{
    font-size: clamp(1.7rem, 2.5vw, 2.6rem); font-weight: 800;
    letter-spacing: -0.03em; line-height: 1.08;
    color: {TEXT}; margin: 0 0 0.65rem;
}}
.lila-hero h1 em {{ font-style:normal; color:{PRIMARY}; }}
.lila-hero p {{ font-size: 0.87rem; color: {MUTED}; max-width: 48ch; line-height: 1.8; margin:0; }}
.lila-chips {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:1.1rem; }}
.lila-chip {{
    font-size:0.58rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    padding:3px 11px; border-radius:999px;
    background:{CHIP_BG}; color:{CHIP_COLOR}; border:1px solid {PRIMARY_BR};
}}
.lila-chip.n {{ background:{SURFACE2}; color:{MUTED}; border-color:{BORDER}; }}

/* STEP DIVIDERS */
.lila-step {{
    display:flex; align-items:center; gap:10px;
    margin: 1.6rem 0 0.8rem;
}}
.lila-step-num {{
    width:22px; height:22px; border-radius:50%;
    background:{CHIP_BG}; border:1px solid {PRIMARY_BR};
    display:flex; align-items:center; justify-content:center;
    font-size:0.6rem; font-weight:800; color:{PRIMARY}; flex-shrink:0;
}}
.lila-step-label {{
    font-size:0.58rem; font-weight:700; letter-spacing:0.18em;
    text-transform:uppercase; color:{PRIMARY};
}}
.lila-step-line {{ flex:1; height:1px; background:{BORDER}; }}

/* METRIC CARDS */
.lila-metrics {{ display:flex; gap:10px; flex-wrap:wrap; margin:0.75rem 0; }}
.lila-metric {{
    background:{METRIC_BG}; border:1px solid {BORDER};
    border-radius:10px; padding:11px 16px; min-width:110px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.lila-mlabel {{ font-size:0.52rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase; color:{FAINT}; margin-bottom:4px; }}
.lila-mvalue {{ font-size:0.85rem; font-weight:700; color:{TEXT}; font-family:'JetBrains Mono',monospace; }}
.lila-mvalue.p {{ color:{PRIMARY}; }}

/* CRS BADGE */
.lila-crs-badge {{
    display:inline-flex; align-items:center; gap:10px;
    background:{INFO_BG}; border:1px solid {PRIMARY_BR};
    border-radius:10px; padding:10px 16px;
    font-size:0.78rem; color:{MUTED}; margin:0.6rem 0;
}}
.lila-crs-badge strong {{
    font-family:'JetBrains Mono',monospace;
    font-size:0.83rem; color:{PRIMARY};
}}

/* INFO BOX */
.lila-info {{
    background:{INFO_BG}; border:1px solid {PRIMARY_BR};
    border-radius:9px; padding:10px 14px;
    font-size:0.78rem; color:{PRIMARY};
    margin-bottom:1rem; line-height:1.7;
}}

/* BEFORE/AFTER CRS CARD */
.lila-compare {{
    display:grid; grid-template-columns:1fr auto 1fr;
    gap:0; border:1px solid {BORDER};
    border-radius:12px; overflow:hidden;
    margin:0.75rem 0; box-shadow:{SHADOW};
}}
.lila-compare-side {{
    padding:16px 20px; background:{SURFACE};
}}
.lila-compare-side.right {{ background:{METRIC_BG}; }}
.lila-compare-arrow {{
    display:flex; align-items:center; justify-content:center;
    padding:0 14px; background:{SURFACE2};
    font-size:1.1rem; color:{PRIMARY}; font-weight:700;
}}
.lila-compare-label {{
    font-size:0.5rem; font-weight:700; letter-spacing:0.15em;
    text-transform:uppercase; color:{FAINT}; margin-bottom:6px;
}}
.lila-compare-crs {{
    font-family:'JetBrains Mono',monospace;
    font-size:0.9rem; font-weight:700; color:{PRIMARY};
    margin-bottom:3px;
}}
.lila-compare-name {{ font-size:0.73rem; color:{MUTED}; line-height:1.4; }}

/* DOWNLOAD BUTTON */
.lila-dl-wrap {{ margin-top:1rem; }}
.lila-dl-btn {{
    display:inline-flex; align-items:center; gap:9px;
    background:{PRIMARY}; color:#fff !important;
    border-radius:10px; padding:0.65rem 1.4rem;
    font-size:0.85rem; font-weight:700;
    box-shadow:0 4px 14px {PRIMARY_BG};
    text-decoration:none; cursor:pointer;
    border:none; transition:background 0.18s;
}}

/* HISTORY TABLE */
.lila-tbl {{ border:1px solid {BORDER}; border-radius:12px; overflow:hidden; margin-top:0.6rem; }}
.lila-tr {{ display:grid; grid-template-columns:2fr 1fr 1fr 0.8fr 0.5fr; border-bottom:1px solid {BORDER}; font-size:0.75rem; }}
.lila-tr:last-child {{ border-bottom:none; }}
.lila-th {{ font-size:0.52rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase; color:{FAINT}; padding:9px 11px; background:{HIST_HEAD}; }}
.lila-td {{ padding:10px 11px; color:{TEXT}; }}
.lila-tag {{
    font-family:'JetBrains Mono',monospace; font-size:0.65rem;
    font-weight:700; background:{TAG_BG}; color:{PRIMARY};
    padding:2px 8px; border-radius:5px;
}}
.lila-tag.n {{ background:{SURFACE2}; color:{MUTED}; font-family:'Inter',sans-serif; font-size:0.6rem; text-transform:uppercase; letter-spacing:0.07em; border:1px solid {BORDER}; }}
.lila-ok {{ font-size:0.68rem; color:{SUCCESS}; font-weight:700; }}

/* SIDEBAR LOGO */
.lila-logo {{
    display:flex; align-items:center; gap:10px;
    padding:0 0 1.25rem; margin-bottom:1.25rem;
    border-bottom:1px solid {BORDER};
}}
.lila-logo-mark {{
    width:32px; height:32px; border-radius:8px;
    background:{PRIMARY}; display:flex; align-items:center;
    justify-content:center; flex-shrink:0;
}}
.lila-logo-text {{ font-size:0.88rem; font-weight:800; color:{TEXT}; letter-spacing:-0.02em; }}
.lila-logo-sub {{ font-size:0.58rem; color:{FAINT}; font-weight:500; margin-top:1px; }}

/* SIDEBAR NAV */
.lila-nav-item {{
    display:flex; align-items:center; gap:9px;
    padding:9px 12px; border-radius:8px;
    font-size:0.78rem; font-weight:500; color:{MUTED};
    margin-bottom:3px; cursor:default;
}}
.lila-nav-item.active {{
    background:{INFO_BG}; color:{PRIMARY};
    font-weight:700; border:1px solid {PRIMARY_BR};
}}
.lila-nav-dot {{ width:7px; height:7px; border-radius:50%; background:{BORDER}; flex-shrink:0; }}
.lila-nav-dot.active {{ background:{PRIMARY}; }}

/* FOOTER */
.lila-footer {{
    border-top:1px solid {BORDER}; margin-top:2.5rem;
    padding-top:1.1rem; display:flex; justify-content:space-between;
    align-items:center; flex-wrap:wrap; gap:8px;
}}
.lila-footer-l {{ font-size:0.67rem; color:{FAINT}; }}
.lila-footer-r {{ display:flex; gap:18px; }}
.lila-footer-r a {{
    font-size:0.6rem; font-weight:700; letter-spacing:0.1em;
    text-transform:uppercase; color:{FAINT}; text-decoration:none;
}}
.lila-footer-r a:hover {{ color:{PRIMARY}; }}

/* Streamlit overrides */
div[data-testid="stButton"] button {{
    background:{BTN_BG} !important; color:#fff !important;
    border:none !important; border-radius:9px !important;
    font-weight:600 !important; font-size:0.82rem !important;
    padding:0.48rem 1.2rem !important;
    box-shadow:0 2px 8px {PRIMARY_BG} !important;
}}
div[data-testid="stButton"] button:hover {{ background:{BTN_HOVER} !important; }}
div[data-testid="stButton"] button:disabled {{
    background:{METRIC_BG} !important; color:{FAINT} !important; box-shadow:none !important;
}}
div[data-testid="stDownloadButton"] > button {{
    background:{PRIMARY} !important; color:#fff !important;
    border:none !important; border-radius:9px !important;
    font-size:0.85rem !important; font-weight:700 !important;
    padding:0.6rem 1.4rem !important;
    box-shadow:0 4px 14px {PRIMARY_BG} !important; width:100%;
}}
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stFileUploader"] label {{
    font-size:0.58rem !important; font-weight:700 !important;
    letter-spacing:0.14em !important; text-transform:uppercase !important;
    color:{FAINT} !important;
}}
div[data-testid="stFileUploader"] {{
    border:2px dashed {BORDER} !important;
    border-radius:12px !important;
    background:{SURFACE} !important;
    padding:1rem !important;
    transition:border-color 0.2s !important;
}}
div[data-testid="stFileUploader"]:hover {{ border-color:{PRIMARY} !important; }}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    # Logo
    st.markdown(f"""
    <div class="lila-logo">
      <div class="lila-logo-mark">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
        </svg>
      </div>
      <div>
        <div class="lila-logo-text">Lila CRS</div>
        <div class="lila-logo-sub">Coordinate Reprojection</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Dark mode toggle
    dark_label = "🌙 Dark Mode" if not st.session_state.dark else "☀️ Light Mode"
    if st.button(dark_label, key="toggle_dark"):
        st.session_state.dark = not st.session_state.dark
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Nav
    steps = [
        ("1", "Upload Files", True),
        ("2", "Detect & Configure CRS", False),
        ("3", "Convert & Download", False),
    ]
    for num, label, active in steps:
        cls = "active" if active else ""
        dot_cls = "active" if active else ""
        st.markdown(f"""
        <div class="lila-nav-item {cls}">
          <div class="lila-nav-dot {dot_cls}"></div>
          <span><strong>{num}.</strong> {label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.58rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:{FAINT};margin-bottom:8px;'>Supported Formats</div>", unsafe_allow_html=True)
    for fmt, desc in [("GeoTIFF", ".tif / .tiff"), ("GeoJSON", ".geojson"), ("Shapefile", ".shp + parts"), ("GeoPackage", "output only")]:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid {BORDER};">
          <span style="font-size:0.75rem;font-weight:600;color:{TEXT};">{fmt}</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:{FAINT};">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.65rem;color:{FAINT};line-height:1.8;">
      <a href="https://epsg.io" target="_blank" style="color:{PRIMARY};font-weight:700;text-decoration:none;">EPSG.io</a> — Find CRS codes<br>
      <a href="https://proj.org" target="_blank" style="color:{PRIMARY};font-weight:700;text-decoration:none;">PROJ</a> — Reprojection engine<br>
      <a href="https://github.com/Athithiyanmr/Lila-crs-converter" target="_blank" style="color:{PRIMARY};font-weight:700;text-decoration:none;">GitHub</a> — Source code
    </div>
    """, unsafe_allow_html=True)

# =========================
# MAIN CONTENT
# =========================

# Hero
st.markdown(f"""
<div class="lila-hero">
  <div class="lila-eyebrow"><span></span>Lila Geospatial Platform</div>
  <h1>Reproject <em>Spatial Data</em><br>with Precision</h1>
  <p>Upload GeoTIFF, GeoJSON, or Shapefiles and instantly convert to any EPSG coordinate reference system.</p>
  <div class="lila-chips">
    <span class="lila-chip">GeoTIFF</span>
    <span class="lila-chip">GeoJSON</span>
    <span class="lila-chip">Shapefile</span>
    <span class="lila-chip n">GeoPackage out</span>
    <span class="lila-chip n">Any EPSG</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ---- STEP 1 ----
st.markdown(f"""
<div class="lila-step">
  <div class="lila-step-num">1</div>
  <div class="lila-step-label">Upload Files</div>
  <div class="lila-step-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="lila-info">
  📌 For Shapefiles, upload <strong>all four parts together</strong>:
  &nbsp;<code>.shp</code>&nbsp;·&nbsp;<code>.shx</code>&nbsp;·&nbsp;<code>.dbf</code>&nbsp;·&nbsp;<code>.prj</code>
</div>
""", unsafe_allow_html=True)

files = st.file_uploader(
    "Drag & drop files here, or click to browse",
    type=["tif", "tiff", "geojson", "shp", "shx", "dbf", "prj"],
    accept_multiple_files=True,
)

if files:
    total_mb = sum(f.size for f in files) / (1024 * 1024)
    exts = ", ".join(sorted(set(f.name.rsplit(".", 1)[-1].upper() for f in files)))
    st.markdown(f"""
    <div class="lila-metrics">
      <div class="lila-metric"><div class="lila-mlabel">Files</div><div class="lila-mvalue">{len(files)}</div></div>
      <div class="lila-metric"><div class="lila-mlabel">Total Size</div><div class="lila-mvalue">{total_mb:.1f} MB</div></div>
      <div class="lila-metric"><div class="lila-mlabel">Types</div><div class="lila-mvalue p">{exts}</div></div>
    </div>
    """, unsafe_allow_html=True)
    if total_mb > 200:
        st.warning(f"⚠️ **{total_mb:.1f} MB** total — large files may take several minutes.")

# ---- STEP 2 ----
st.markdown(f"""
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
                    res = requests.post(f"{API}/detect-crs", files=[("files", f) for f in files], timeout=300)
                if res.status_code == 200:
                    st.session_state.detected_crs = res.json().get("crs", "Unknown")
                else:
                    st.error(res.json().get("detail", res.text))
            except Exception as e:
                st.error(f"Server error: {e}")

    if st.session_state.detected_crs:
        src_name = EPSG_NAMES.get(st.session_state.detected_crs, "Unknown projection")
        st.markdown(f"""
        <div class="lila-crs-badge">
          🛡️&nbsp; Source CRS detected: &nbsp;<strong>{st.session_state.detected_crs}</strong>
          &nbsp;—&nbsp; <span style="font-size:0.75rem;">{src_name}</span>
        </div>
        """, unsafe_allow_html=True)

    col_crs, col_fmt = st.columns(2)

    with col_crs:
        preset = st.selectbox("Target CRS (preset)", PRESET_CRS)
        if preset == "Custom (enter below)":
            custom_epsg = st.text_input("Custom EPSG code", placeholder="e.g. EPSG:7760", help="Find codes at epsg.io")
            target_crs = custom_epsg.strip().upper() if custom_epsg else ""
            if target_crs and not target_crs.startswith("EPSG:"):
                st.warning("⚠️ Must start with ‘EPSG:’ — e.g. EPSG:4326")
                target_crs = ""
        else:
            target_crs = preset.split()[0]

        # Live EPSG name lookup
        if target_crs and target_crs in EPSG_NAMES:
            st.markdown(f"""
            <div style="font-size:0.72rem;color:{PRIMARY};margin-top:4px;
                        background:{INFO_BG};border:1px solid {PRIMARY_BR};
                        border-radius:6px;padding:6px 10px;font-family:'JetBrains Mono',monospace;">
              ✔️&nbsp; {EPSG_NAMES[target_crs]}
            </div>
            """, unsafe_allow_html=True)
        elif target_crs and target_crs.startswith("EPSG:"):
            st.markdown(f"""
            <div style="font-size:0.72rem;color:{FAINT};margin-top:4px;padding:5px 10px;">
              Custom code — verify at <a href="https://epsg.io/{target_crs.replace('EPSG:','')}" target="_blank" style="color:{PRIMARY};">epsg.io/{target_crs.replace('EPSG:','')}</a>
            </div>
            """, unsafe_allow_html=True)

    with col_fmt:
        output_format_ui = st.selectbox("Output Format", ["GeoJSON (.geojson)", "GeoPackage (.gpkg)", "Shapefile (.zip)"])

    out_fmt = "geojson" if "GeoJSON" in output_format_ui else ("gpkg" if "GeoPackage" in output_format_ui else "shapefile")
    st.session_state.target_crs_final = target_crs

else:
    st.caption("Upload files above to configure CRS options.")
    target_crs = ""
    out_fmt = "geojson"

# ---- STEP 3 ----
st.markdown(f"""
<div class="lila-step">
  <div class="lila-step-num">3</div>
  <div class="lila-step-label">Convert &amp; Download</div>
  <div class="lila-step-line"></div>
</div>
""", unsafe_allow_html=True)

convert_ready = bool(files and target_crs)

if not files:
    st.caption("Complete Step 1 to enable conversion.")
elif not target_crs:
    st.caption("Select a target CRS in Step 2 to enable conversion.")

if convert_ready:
    if st.button("♻️ Convert CRS", disabled=not convert_ready):
        try:
            with st.spinner("Reprojecting… please wait."):
                res = requests.post(
                    f"{API}/convert",
                    files=[("files", f) for f in files],
                    data={"target_crs": target_crs, "output_format": out_fmt},
                    timeout=1800
                )
            if res.status_code == 200:
                st.success("✅ Reprojection complete!")
                st.session_state.converted = True
                st.session_state.history.insert(0, {
                    "files": ", ".join(f.name for f in files),
                    "source": st.session_state.detected_crs or "—",
                    "target": target_crs,
                    "format": out_fmt,
                })
                ext_map = {"geojson": "reprojected.geojson", "gpkg": "reprojected.gpkg", "shapefile": "reprojected.zip"}
                out_name = "reprojected.tif" if any(f.name.lower().endswith((".tif",".tiff")) for f in files) else ext_map[out_fmt]

                # Before / After CRS comparison card
                src = st.session_state.detected_crs or "—"
                src_name = EPSG_NAMES.get(src, "Original projection")
                tgt_name = EPSG_NAMES.get(target_crs, "Reprojected")
                st.markdown(f"""
                <div class="lila-compare">
                  <div class="lila-compare-side">
                    <div class="lila-compare-label">Source CRS</div>
                    <div class="lila-compare-crs" style="opacity:0.6">{src}</div>
                    <div class="lila-compare-name">{src_name}</div>
                  </div>
                  <div class="lila-compare-arrow">→</div>
                  <div class="lila-compare-side right">
                    <div class="lila-compare-label">Target CRS</div>
                    <div class="lila-compare-crs">{target_crs}</div>
                    <div class="lila-compare-name">{tgt_name}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    "⬇️ Download Reprojected File",
                    data=res.content,
                    file_name=out_name,
                    mime="application/octet-stream"
                )
            else:
                st.error(res.json().get("detail", res.text))
        except Exception as e:
            st.error(f"Server error: {e}")

# ---- HISTORY ----
if st.session_state.history:
    st.markdown(f"""
    <div class="lila-step" style="margin-top:1.8rem;">
      <div class="lila-step-num" style="background:{SURFACE2};color:{FAINT};border-color:{BORDER};">↺</div>
      <div class="lila-step-label">Session History</div>
      <div class="lila-step-line"></div>
    </div>
    """, unsafe_allow_html=True)

    rows = ""
    for h in st.session_state.history:
        rows += f"""
        <div class="lila-tr">
          <div class="lila-td" style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{h['files']}</div>
          <div class="lila-td"><span class="lila-tag" style="opacity:0.65">{h['source']}</span></div>
          <div class="lila-td"><span class="lila-tag">{h['target']}</span></div>
          <div class="lila-td"><span class="lila-tag n">{h['format']}</span></div>
          <div class="lila-td"><span class="lila-ok">✓ Done</span></div>
        </div>"""

    st.markdown(f"""
    <div class="lila-tbl">
      <div class="lila-tr">
        <div class="lila-th">Files</div>
        <div class="lila-th">Source CRS</div>
        <div class="lila-th">Target CRS</div>
        <div class="lila-th">Format</div>
        <div class="lila-th">Status</div>
      </div>{rows}
    </div>
    """, unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown(f"""
<div class="lila-footer">
  <div class="lila-footer-l">Built by <strong>Athithiyan MR</strong> — Lila Geospatial Platform</div>
  <div class="lila-footer-r">
    <a href="https://epsg.io" target="_blank">EPSG.io</a>
    <a href="https://proj.org" target="_blank">PROJ Docs</a>
    <a href="https://github.com/Athithiyanmr/Lila-crs-converter" target="_blank">GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)
