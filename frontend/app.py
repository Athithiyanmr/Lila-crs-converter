import streamlit as st
import requests

API = "http://geocrs-api:8000"
st.set_page_config(
    page_title="Lila CRS Converter",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

for key, val in [("detected_crs", None), ("history", []), ("target_crs_final", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================
# AUROVILLE CONSULTING PALETTE
# Deep forest green + warm gold + cream parchment
# ============================================================
G    = "#0b553d"          # Auroville deep green (primary)
GD   = "#084430"          # darker green hover
GBG  = "rgba(11,85,61,0.07)"
GBR  = "rgba(11,85,61,0.18)"
GOLD = "#bf9000"          # Auroville warm gold (accent)
GOLD_BG = "rgba(191,144,0,0.08)"
BG   = "#faf8f3"          # warm cream
S1   = "#ffffff"
S2   = "#f4f1ea"          # parchment surface
S3   = "#ebe7de"          # deeper parchment
BD   = "#dbd5c8"          # warm border
BD2  = "#c9c2b3"
TX   = "#1c1a14"          # near-black warm text
MU   = "#4d4637"          # muted warm brown
FA   = "#9a9080"          # faint warm gray
MO   = "'JetBrains Mono', monospace"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─ GLOBAL ──────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background: {BG} !important;
    color: {TX} !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    max-width: 740px !important;
    padding: 2rem 1.5rem 3rem !important;
}}

/* ─ NAV BAR ────────────────────────────────────── */
.lila-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    margin-bottom: 1.75rem;
    border-bottom: 1px solid {BD};
}}
.lila-brand {{ display: flex; align-items: center; gap: 10px; }}
.lila-mark {{
    width: 30px; height: 30px;
    background: {G};
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
}}
.lila-brand-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem; font-weight: 600;
    color: {TX}; letter-spacing: 0.01em; line-height: 1;
}}
.lila-brand-sub {{
    font-size: 0.56rem; color: {FA};
    text-transform: uppercase; letter-spacing: 0.12em; margin-top: 2px;
}}
.lila-nav-links {{ display: flex; gap: 18px; }}
.lila-nav-links a {{
    font-size: 0.68rem; font-weight: 500; color: {MU};
    text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;
    transition: color 0.15s;
}}
.lila-nav-links a:hover {{ color: {G}; }}

/* ─ PAGE TITLE ──────────────────────────────────── */
.lila-title {{ margin-bottom: 1.75rem; }}
.lila-title h1 {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.5rem; font-weight: 500;
    line-height: 1.1; color: {TX};
    letter-spacing: -0.01em; margin: 0 0 0.45rem;
}}
.lila-title h1 em {{ font-style: italic; color: {G}; }}
.lila-title p {{
    font-size: 0.84rem; color: {MU};
    line-height: 1.75; margin: 0;
    max-width: 54ch;
}}
.lila-gold-rule {{
    width: 40px; height: 2px;
    background: {GOLD};
    margin: 0.75rem 0;
    border-radius: 1px;
}}

/* ─ SECTION LABEL ──────────────────────────────── */
.lila-section {{
    display: flex; align-items: center; gap: 9px;
    margin: 1.75rem 0 0.75rem;
}}
.lila-section-num {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.72rem; font-weight: 500;
    color: {GOLD}; letter-spacing: 0.05em;
}}
.lila-section-name {{
    font-size: 0.54rem; font-weight: 700;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: {G};
}}
.lila-section-line {{
    flex: 1; height: 1px; background: {BD};
}}

/* ─ HINT BOX ───────────────────────────────────── */
.lila-hint {{
    font-size: 0.76rem; color: {MU};
    background: {GBG}; border: 1px solid {GBR};
    border-left: 3px solid {G};
    border-radius: 0 6px 6px 0;
    padding: 8px 12px; margin-bottom: 0.75rem; line-height: 1.65;
}}

/* ─ FILE STATS ────────────────────────────────── */
.lila-stats {{ display: flex; gap: 6px; margin: 0.6rem 0; }}
.lila-stat {{
    background: {S1}; border: 1px solid {BD};
    border-radius: 7px; padding: 9px 14px; flex: 1; text-align: center;
}}
.lila-stat-v {{
    font-size: 1.05rem; font-weight: 600;
    color: {TX}; font-family: {MO}; line-height: 1.2;
}}
.lila-stat-v.g {{ color: {G}; }}
.lila-stat-l {{
    font-size: 0.49rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: {FA}; margin-top: 3px;
}}

/* ─ CRS DETECTED ─────────────────────────────── */
.lila-detected {{
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    background: {GBG}; border: 1px solid {GBR};
    border-radius: 7px; padding: 9px 13px;
    margin: 0.55rem 0; font-size: 0.79rem; color: {MU};
}}
.lila-detected code {{
    font-family: {MO}; font-size: 0.81rem;
    font-weight: 600; color: {G};
}}
.lila-detected .sep {{
    color: {BD2}; font-size: 0.7rem;
}}

/* ─ EPSG NOTE ─────────────────────────────────── */
.lila-epsg-note {{
    font-size: 0.68rem; color: {G};
    background: {GBG}; border: 1px solid {GBR};
    border-radius: 5px; padding: 4px 9px;
    font-family: {MO}; margin-top: 4px; display: inline-block;
}}

/* ─ RESULT CARD ───────────────────────────────── */
.lila-result {{
    display: grid; grid-template-columns: 1fr 32px 1fr;
    border: 1px solid {BD}; border-radius: 10px;
    overflow: hidden; margin: 0.75rem 0;
    box-shadow: 0 2px 10px rgba(11,85,61,0.06);
}}
.lila-rs {{ padding: 15px 18px; background: {S1}; }}
.lila-rs.b {{ background: {S2}; }}
.lila-rarrow {{
    display: flex; align-items: center; justify-content: center;
    background: {S3}; color: {GOLD}; font-size: 0.95rem; font-weight: 700;
}}
.lila-rs-label {{
    font-size: 0.48rem; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: {FA}; margin-bottom: 4px;
}}
.lila-rs-crs {{
    font-family: {MO}; font-size: 0.88rem;
    font-weight: 600; color: {G}; margin-bottom: 2px;
}}
.lila-rs-name {{ font-size: 0.71rem; color: {MU}; line-height: 1.4; }}

/* ─ HISTORY TABLE ──────────────────────────────── */
.lila-history {{
    border: 1px solid {BD}; border-radius: 10px;
    overflow: hidden; margin-top: 0.5rem;
}}
.lila-hrow {{
    display: grid;
    grid-template-columns: 2fr 0.9fr 0.9fr 0.7fr 0.45fr;
    border-bottom: 1px solid {BD}; font-size: 0.73rem;
}}
.lila-hrow:last-child {{ border-bottom: none; }}
.lila-hh {{
    font-size: 0.48rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: {FA}; padding: 8px 10px; background: {S3};
}}
.lila-hd {{ padding: 9px 10px; color: {TX}; background: {S1}; }}
.lila-badge {{
    display: inline-block; font-family: {MO};
    font-size: 0.62rem; font-weight: 600;
    background: {GBG}; color: {G};
    border-radius: 4px; padding: 1px 6px;
}}
.lila-badge.n {{
    background: {S3}; color: {MU};
    font-family: 'Inter', sans-serif; font-size: 0.57rem;
    text-transform: uppercase; letter-spacing: 0.06em;
    border: 1px solid {BD2};
}}
.lila-ok {{ font-size: 0.65rem; color: {G}; font-weight: 600; }}

/* ─ FOOTER ───────────────────────────────────────── */
.lila-footer {{
    margin-top: 3rem; padding-top: 1rem;
    border-top: 1px solid {BD};
    display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 6px;
}}
.lila-footer span {{ font-size: 0.63rem; color: {FA}; }}
.lila-footer-links {{ display: flex; gap: 14px; }}
.lila-footer-links a {{
    font-size: 0.57rem; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: {FA}; text-decoration: none;
}}
.lila-footer-links a:hover {{ color: {G}; }}

/* ─ STREAMLIT WIDGET OVERRIDES ─────────────────── */
div[data-testid="stButton"] button {{
    background: {G} !important; color: #fff !important;
    border: none !important; border-radius: 7px !important;
    font-weight: 600 !important; font-size: 0.81rem !important;
    padding: 0.44rem 1.1rem !important;
    transition: background 0.15s !important;
}}
div[data-testid="stButton"] button:hover {{ background: {GD} !important; }}
div[data-testid="stButton"] button:disabled {{
    background: {S3} !important; color: {FA} !important;
}}
div[data-testid="stDownloadButton"] > button {{
    background: {G} !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    padding: 0.55rem 1.3rem !important; width: 100% !important;
    transition: background 0.15s !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{ background: {GD} !important; }}
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stFileUploader"] label {{
    font-size: 0.52rem !important; font-weight: 700 !important;
    letter-spacing: 0.16em !important; text-transform: uppercase !important;
    color: {FA} !important;
}}
div[data-testid="stFileUploader"] > div {{
    border: 1.5px dashed {BD2} !important;
    border-radius: 10px !important; background: {S2} !important;
    transition: border-color 0.18s !important;
}}
div[data-testid="stFileUploader"] > div:hover {{ border-color: {G} !important; }}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div > input {{
    border-color: {BD2} !important; border-radius: 7px !important;
    background: {S1} !important;
}}
/* Force light background on all Streamlit containers */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {{ background: {BG} !important; }}
</style>
""", unsafe_allow_html=True)

# ── NAV ─────────────────────────────────────────────────
st.markdown(f"""
<div class="lila-nav">
  <div class="lila-brand">
    <div class="lila-mark">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none"
           stroke="white" stroke-width="2.2"
           stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10
                 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
    </div>
    <div>
      <div class="lila-brand-name">Lila CRS</div>
      <div class="lila-brand-sub">Geospatial Platform</div>
    </div>
  </div>
  <div class="lila-nav-links">
    <a href="https://epsg.io" target="_blank">EPSG.io</a>
    <a href="https://github.com/Athithiyanmr/Lila-crs-converter" target="_blank">GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TITLE ────────────────────────────────────────────────
st.markdown(f"""
<div class="lila-title">
  <h1>Reproject <em>Spatial Data</em><br>with Precision</h1>
  <div class="lila-gold-rule"></div>
  <p>Convert GeoTIFF, GeoJSON, or Shapefiles to any EPSG coordinate system — fast and reliable.</p>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: UPLOAD ───────────────────────────────────────
st.markdown(f"""
<div class="lila-section">
  <span class="lila-section-num">01</span>
  <span class="lila-section-name">Upload Files</span>
  <span class="lila-section-line"></span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="lila-hint">
  For Shapefiles, upload all parts together:
  <code>.shp</code> &middot; <code>.shx</code> &middot; <code>.dbf</code> &middot; <code>.prj</code>
</div>
""", unsafe_allow_html=True)

files = st.file_uploader(
    "Drop files here or click to browse",
    type=["tif", "tiff", "geojson", "shp", "shx", "dbf", "prj"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

if files:
    total_mb = sum(f.size for f in files) / 1024 / 1024
    exts = ", ".join(sorted({f.name.rsplit(".", 1)[-1].upper() for f in files}))
    st.markdown(f"""
    <div class="lila-stats">
      <div class="lila-stat">
        <div class="lila-stat-v">{len(files)}</div>
        <div class="lila-stat-l">Files</div>
      </div>
      <div class="lila-stat">
        <div class="lila-stat-v">{total_mb:.1f} MB</div>
        <div class="lila-stat-l">Size</div>
      </div>
      <div class="lila-stat">
        <div class="lila-stat-v g">{exts}</div>
        <div class="lila-stat-l">Types</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if total_mb > 200:
        st.warning(f"⚠️ {total_mb:.1f} MB — large files may take several minutes.")

# ── STEP 2: DETECT & CONFIGURE ───────────────────────────
st.markdown(f"""
<div class="lila-section">
  <span class="lila-section-num">02</span>
  <span class="lila-section-name">Detect &amp; Configure CRS</span>
  <span class="lila-section-line"></span>
</div>
""", unsafe_allow_html=True)

if files:
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Detect Source CRS"):
            try:
                with st.spinner("Detecting…"):
                    r = requests.post(f"{API}/detect-crs",
                                      files=[("files", f) for f in files],
                                      timeout=300)
                if r.status_code == 200:
                    st.session_state.detected_crs = r.json().get("crs", "Unknown")
                else:
                    st.error(r.json().get("detail", r.text))
            except Exception as e:
                st.error(f"Server error: {e}")

    if st.session_state.detected_crs:
        name = EPSG_NAMES.get(st.session_state.detected_crs, "Unknown projection")
        st.markdown(f"""
        <div class="lila-detected">
          <span>Source CRS</span>
          <code>{st.session_state.detected_crs}</code>
          <span class="sep">—</span>
          <span>{name}</span>
        </div>
        """, unsafe_allow_html=True)

    col_crs, col_fmt = st.columns(2)
    with col_crs:
        preset = st.selectbox("Target CRS", PRESET_CRS)
        if preset == "Custom (enter below)":
            raw = st.text_input("Custom EPSG", placeholder="e.g. EPSG:7760")
            target_crs = raw.strip().upper() if raw else ""
            if target_crs and not target_crs.startswith("EPSG:"):
                st.warning("Must start with EPSG: — e.g. EPSG:4326")
                target_crs = ""
        else:
            target_crs = preset.split()[0]

        if target_crs in EPSG_NAMES:
            st.markdown(
                f'<div class="lila-epsg-note">✔ {EPSG_NAMES[target_crs]}</div>',
                unsafe_allow_html=True)
        elif target_crs.startswith("EPSG:"):
            code = target_crs.replace("EPSG:", "")
            st.markdown(
                f'<div style="font-size:0.67rem;color:{FA};margin-top:3px;">'
                f'Verify at <a href="https://epsg.io/{code}" target="_blank" '
                f'style="color:{G};">epsg.io/{code}</a></div>',
                unsafe_allow_html=True)

    with col_fmt:
        fmt_ui = st.selectbox("Output Format",
                              ["GeoJSON (.geojson)", "GeoPackage (.gpkg)", "Shapefile (.zip)"])

    out_fmt = ("geojson" if "GeoJSON" in fmt_ui
               else "gpkg" if "GeoPackage" in fmt_ui
               else "shapefile")
    st.session_state.target_crs_final = target_crs
else:
    st.caption("Upload files above to continue.")
    target_crs, out_fmt = "", "geojson"

# ── STEP 3: CONVERT ──────────────────────────────────────
st.markdown(f"""
<div class="lila-section">
  <span class="lila-section-num">03</span>
  <span class="lila-section-name">Convert &amp; Download</span>
  <span class="lila-section-line"></span>
</div>
""", unsafe_allow_html=True)

if not files:
    st.caption("Complete Step 1 to enable conversion.")
elif not target_crs:
    st.caption("Select a target CRS to enable conversion.")
else:
    if st.button("Convert CRS"):
        try:
            with st.spinner("Reprojecting… please wait."):
                r = requests.post(
                    f"{API}/convert",
                    files=[("files", f) for f in files],
                    data={"target_crs": target_crs, "output_format": out_fmt},
                    timeout=1800,
                )
            if r.status_code == 200:
                st.success("Reprojection complete.")
                st.session_state.history.insert(0, {
                    "files":  ", ".join(f.name for f in files),
                    "source": st.session_state.detected_crs or "—",
                    "target": target_crs,
                    "format": out_fmt,
                })
                ext_map = {"geojson": "reprojected.geojson",
                           "gpkg":    "reprojected.gpkg",
                           "shapefile": "reprojected.zip"}
                out_name = ("reprojected.tif"
                            if any(f.name.lower().endswith((".tif", ".tiff")) for f in files)
                            else ext_map[out_fmt])

                src = st.session_state.detected_crs or "—"
                sn  = EPSG_NAMES.get(src, "Original")
                tn  = EPSG_NAMES.get(target_crs, "Reprojected")
                st.markdown(f"""
                <div class="lila-result">
                  <div class="lila-rs">
                    <div class="lila-rs-label">Source</div>
                    <div class="lila-rs-crs" style="opacity:.55">{src}</div>
                    <div class="lila-rs-name">{sn}</div>
                  </div>
                  <div class="lila-rarrow">&rarr;</div>
                  <div class="lila-rs b">
                    <div class="lila-rs-label">Target</div>
                    <div class="lila-rs-crs">{target_crs}</div>
                    <div class="lila-rs-name">{tn}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    "⬇ Download Reprojected File",
                    data=r.content,
                    file_name=out_name,
                    mime="application/octet-stream",
                )
            else:
                st.error(r.json().get("detail", r.text))
        except Exception as e:
            st.error(f"Server error: {e}")

# ── HISTORY ──────────────────────────────────────────────
if st.session_state.history:
    st.markdown(f"""
    <div class="lila-section" style="margin-top:1.75rem;">
      <span class="lila-section-num" style="color:{FA};">&#x21BA;</span>
      <span class="lila-section-name">Session History</span>
      <span class="lila-section-line"></span>
    </div>
    """, unsafe_allow_html=True)
    rows = "".join(f"""
    <div class="lila-hrow">
      <div class="lila-hd" style="font-family:'JetBrains Mono',monospace;
           font-size:0.65rem;overflow:hidden;text-overflow:ellipsis;
           white-space:nowrap;">{h['files']}</div>
      <div class="lila-hd"><span class="lila-badge" style="opacity:.55">{h['source']}</span></div>
      <div class="lila-hd"><span class="lila-badge">{h['target']}</span></div>
      <div class="lila-hd"><span class="lila-badge n">{h['format']}</span></div>
      <div class="lila-hd"><span class="lila-ok">✓</span></div>
    </div>""" for h in st.session_state.history)
    st.markdown(f"""
    <div class="lila-history">
      <div class="lila-hrow">
        <div class="lila-hh">File</div>
        <div class="lila-hh">From</div>
        <div class="lila-hh">To</div>
        <div class="lila-hh">Format</div>
        <div class="lila-hh">OK</div>
      </div>{rows}
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown(f"""
<div class="lila-footer">
  <span>Lila Geospatial &mdash; Athithiyan MR</span>
  <div class="lila-footer-links">
    <a href="https://epsg.io" target="_blank">EPSG.io</a>
    <a href="https://proj.org" target="_blank">PROJ</a>
    <a href="https://github.com/Athithiyanmr/Lila-crs-converter" target="_blank">GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)
