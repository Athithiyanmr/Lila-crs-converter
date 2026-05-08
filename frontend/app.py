import streamlit as st
import requests

API = "http://geocrs-api:8000"
st.set_page_config(
    page_title="Lila CRS Converter",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
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

for k, v in [("detected_crs", None), ("history", []), ("target_crs_final", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Design tokens ──────────────────────────────────────────
BG   = "#f2f4ff"
S1   = "#ffffff"
S2   = "#e8ecf8"
S3   = "#dde3f0"
BD   = "#c5cde0"
BD2  = "#b0b9d1"
TX   = "#0B1026"
MU   = "#4a5578"
FA   = "#8090b0"
P    = "#1B6CA8"
PH   = "#145a8f"
PL   = "#e0f0ff"
PLR  = "rgba(27,108,168,0.18)"
PBG  = "rgba(27,108,168,0.07)"
ACC  = "#FFB000"
DARK_BG  = "#0B1026"
DARK_S1  = "#111838"
DARK_S2  = "#18204A"
DARK_P   = "#39C6D6"
MO   = "'JetBrains Mono', 'Consolas', monospace"

st.markdown(f"""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&f[]=cabinet-grotesk@500,700,800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

html, body {{ background: {BG} !important; color: {TX} !important; }}
[class*="css"] {{ font-family: 'General Sans', 'Helvetica Neue', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stAppViewContainer"],[data-testid="stMain"],.main {{ background: {BG} !important; }}
.block-container {{ max-width: 100% !important; padding: 0 !important; margin: 0 !important; }}

.stMarkdown, .stMarkdown p, .stMarkdown span,
[data-testid="stMarkdownContainer"],[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stText"], .stText, span, p, div {{
    color: {TX} !important;
}}

[data-testid="stSelectbox"] label,[data-testid="stSelectbox"] label span,
[data-testid="stSelectbox"] label p {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    color: {FA} !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"],
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {{
    background: {S1} !important; color: {TX} !important;
    border-color: {BD2} !important; border-radius: 8px !important;
    font-size: 0.88rem !important; font-family: 'General Sans', sans-serif !important;
}}
[data-baseweb="popover"] ul li,[data-baseweb="menu"] li,
[data-baseweb="menu"] li span,[data-baseweb="menu"] li div {{
    color: {TX} !important; background: {S1} !important;
    font-size: 0.86rem !important; font-family: 'General Sans', sans-serif !important;
}}
[data-baseweb="menu"] li:hover {{ background: {PBG} !important; }}

[data-testid="stTextInput"] label,[data-testid="stTextInput"] label span,
[data-testid="stTextInput"] label p {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    color: {FA} !important;
}}
[data-testid="stTextInput"] input {{
    background: {S1} !important; color: {TX} !important;
    border-color: {BD2} !important; border-radius: 8px !important;
    font-size: 0.88rem !important; font-family: 'General Sans', sans-serif !important;
}}
[data-testid="stTextInput"] input::placeholder {{ color: {FA} !important; opacity: 1 !important; }}

[data-testid="stFileUploader"] label,[data-testid="stFileUploader"] label span,
[data-testid="stFileUploader"] label p {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.68rem !important; font-weight: 700 !important;
    letter-spacing: 0.13em !important; text-transform: uppercase !important;
    color: {FA} !important;
}}
[data-testid="stFileUploader"] section {{
    border: 1.5px dashed {BD2} !important;
    border-radius: 10px !important; background: {S2} !important;
    transition: border-color 0.2s, background 0.2s !important;
}}
[data-testid="stFileUploader"] section:hover {{
    border-color: {P} !important; background: {PBG} !important;
}}
[data-testid="stFileUploader"] section span,[data-testid="stFileUploader"] section p,
[data-testid="stFileUploader"] section div,[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p {{ color: {MU} !important; font-size: 0.86rem !important; }}
[data-testid="stFileUploaderFile"] span,[data-testid="stFileUploaderFile"] p,
[data-testid="stFileUploaderFile"] div,[data-testid="stFileUploaderFileName"],
[data-testid="stFileUploaderFileData"] {{ color: {TX} !important; font-size: 0.84rem !important; }}

[data-testid="stAlert"] p,[data-testid="stAlert"] span,
.stAlert p, .stSuccess p, .stError p, .stWarning p, .stInfo p {{
    color: {TX} !important; font-size: 0.86rem !important;
}}
[data-testid="stSpinner"] span,[data-testid="stSpinner"] p {{ color: {MU} !important; }}
.stCaption,[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p {{
    font-size: 0.78rem !important; color: {FA} !important;
}}
.lila-right p, .lila-right li, .lila-right .stMarkdown p {{
    font-size: 0.88rem !important; line-height: 1.75 !important; color: {MU} !important;
}}

div[data-testid="stButton"] button {{
    background: {P} !important; color: #ffffff !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'General Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.6rem 1.6rem !important; letter-spacing: 0.01em !important;
    transition: background 0.18s, box-shadow 0.18s, transform 0.18s !important;
    box-shadow: 0 2px 8px rgba(27,108,168,0.22) !important;
}}
div[data-testid="stButton"] button:hover {{
    background: {PH} !important; transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(27,108,168,0.32) !important;
}}
div[data-testid="stButton"] button span {{ color: #ffffff !important; }}

div[data-testid="stDownloadButton"] > button {{
    background: {ACC} !important; color: {DARK_BG} !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.92rem !important; font-weight: 700 !important;
    padding: 0.62rem 1.6rem !important; width: 100% !important;
    box-shadow: 0 2px 8px rgba(255,176,0,0.28) !important;
    transition: opacity 0.15s, transform 0.18s !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    opacity: 0.88 !important; transform: translateY(-2px) !important;
}}
div[data-testid="stDownloadButton"] > button span {{ color: {DARK_BG} !important; }}

/* TOP NAV */
.lila-topbar {{
    position: sticky; top: 0; z-index: 100;
    background: rgba(242,244,255,0.92);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid {BD};
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 2.5rem; height: 62px;
    box-shadow: 0 1px 8px rgba(11,16,38,0.06);
}}
.lila-brand {{ display: flex; align-items: center; gap: 12px; }}
.lila-mark {{
    width: 36px; height: 36px; background: {P};
    border-radius: 8px; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
}}
.lila-brand-name {{
    font-family: 'Cabinet Grotesk', 'Helvetica Neue', sans-serif !important;
    font-size: 1.05rem; font-weight: 800;
    color: {TX} !important; letter-spacing: -0.02em; line-height: 1;
}}
.lila-brand-sub {{
    font-family: {MO}; font-size: 0.6rem;
    color: {FA} !important; letter-spacing: 0.12em;
    text-transform: uppercase; margin-top: 3px;
}}
.lila-nav-links {{ display: flex; align-items: center; gap: 28px; }}
.lila-nav-links a {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.7rem; font-weight: 600; color: {MU} !important;
    text-decoration: none; text-transform: uppercase; letter-spacing: 0.07em;
    transition: color 0.15s; position: relative;
}}
.lila-nav-links a::after {{
    content: ''; position: absolute; bottom: -4px; left: 0;
    width: 0; height: 2px; background: {P}; transition: width 0.3s ease;
}}
.lila-nav-links a:hover {{ color: {P} !important; }}
.lila-nav-links a:hover::after {{ width: 100%; }}

/* LEFT PANEL */
.lila-left {{
    background: linear-gradient(135deg, {DARK_BG} 0%, {DARK_S2} 55%, #1B6CA8 100%);
    padding: 2.8rem 2rem; display: flex; flex-direction: column;
    min-height: calc(100vh - 62px);
}}
.lila-left-logo {{
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-size: 2.1rem; font-weight: 800;
    color: rgba(232,236,255,0.95) !important; line-height: 1.1;
    letter-spacing: -0.03em; margin-bottom: 0.5rem;
}}
.lila-left-logo em {{ font-style: normal; color: {DARK_P} !important; }}
.lila-accent-bar {{
    width: 28px; height: 2.5px; background: {ACC};
    border-radius: 2px; margin: 0.9rem 0 1.1rem;
}}
.lila-left-desc {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.84rem; color: rgba(232,236,255,0.65) !important;
    line-height: 1.8; margin-bottom: 2rem;
}}
.lila-left-feat {{ display: flex; flex-direction: column; gap: 0.9rem; margin-bottom: 2.2rem; }}
.lila-feat {{ display: flex; align-items: flex-start; gap: 10px; }}
.lila-feat-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {ACC}; margin-top: 7px; flex-shrink: 0;
}}
.lila-feat-text {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.82rem; color: rgba(232,236,255,0.7) !important; line-height: 1.6;
}}
.lila-feat-text strong {{
    color: rgba(232,236,255,0.95) !important; font-weight: 600;
    display: block; font-size: 0.86rem; margin-bottom: 1px;
}}

/* Stat grid — ALL numbers white, no orange */
.lila-left-stats {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin-bottom: 2rem;
}}
.lila-left-stat {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; padding: 14px 16px; text-align: center;
}}
.lila-left-stat-v {{
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-size: 1.35rem; font-weight: 800;
    color: rgba(232,236,255,0.95) !important;
    letter-spacing: -0.02em; display: block;
}}
.lila-left-stat-l {{
    font-family: {MO}; font-size: 0.58rem;
    color: rgba(232,236,255,0.45) !important;
    letter-spacing: 0.08em; text-transform: uppercase; margin-top: 3px;
}}
.lila-left-footer {{
    margin-top: auto; font-family: {MO}; font-size: 0.62rem;
    color: rgba(232,236,255,0.28) !important; line-height: 1.7;
}}

/* RIGHT PANEL */
.lila-right {{ background: {BG}; padding: 2.4rem 3rem; overflow-y: auto; }}
.lila-section {{
    display: flex; align-items: center; gap: 12px; margin: 1.8rem 0 0.9rem;
}}
.lila-section:first-child {{ margin-top: 0; }}
.lila-section-num {{
    font-family: {MO}; font-size: 0.7rem; font-weight: 500;
    color: {P} !important; letter-spacing: 0.15em; min-width: 26px;
    text-transform: uppercase;
}}
.lila-section-num::before {{ content: '// '; opacity: 0.5; }}
.lila-section-name {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: {P} !important;
}}
.lila-section-line {{ flex: 1; height: 1px; background: {BD}; }}

.lila-hint {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.84rem; color: {MU} !important;
    background: {PBG}; border: 1px solid {PLR};
    border-left: 3px solid {P}; border-radius: 0 8px 8px 0;
    padding: 11px 15px; margin-bottom: 1rem; line-height: 1.72;
}}
.lila-hint code {{
    font-family: {MO}; font-size: 0.8rem;
    background: rgba(27,108,168,0.10); padding: 2px 6px;
    border-radius: 3px; color: {P} !important;
}}
.lila-hint strong {{ color: {TX} !important; }}

.lila-stats {{ display: flex; gap: 8px; margin: 0.8rem 0; }}
.lila-stat {{
    background: {S1}; border: 1px solid {BD};
    border-radius: 8px; padding: 12px 16px; flex: 1; text-align: center;
    box-shadow: 0 1px 4px rgba(11,16,38,0.05);
}}
.lila-stat-v {{
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-size: 1.1rem; font-weight: 800;
    color: {TX} !important; letter-spacing: -0.01em; line-height: 1.2;
}}
.lila-stat-v.p {{ color: {P} !important; }}
.lila-stat-v.acc {{ color: {ACC} !important; }}
.lila-stat-l {{
    font-family: {MO}; font-size: 0.6rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: {FA} !important; margin-top: 4px;
}}

.lila-detected {{
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    background: {PBG}; border: 1px solid {PLR};
    border-radius: 8px; padding: 11px 15px; margin: 0.7rem 0;
}}
.lila-detected::before {{
    content: ''; width: 7px; height: 7px;
    background: {P}; border-radius: 50%;
    animation: pulse 2s infinite; flex-shrink: 0;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.5; transform: scale(1.5); }}
}}
.lila-detected .dlabel {{
    font-family: {MO}; font-size: 0.65rem; font-weight: 500;
    letter-spacing: 0.1em; text-transform: uppercase; color: {FA} !important;
}}
.lila-detected code {{
    font-family: {MO}; font-size: 0.9rem; font-weight: 700;
    color: {P} !important; background: {PL};
    padding: 2px 8px; border-radius: 4px;
}}
.lila-detected .dname {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.83rem; color: {MU} !important; font-weight: 500;
}}

.lila-epsg-note {{
    font-family: {MO}; font-size: 0.76rem; color: {P} !important;
    background: {PBG}; border: 1px solid {PLR};
    border-radius: 5px; padding: 5px 10px;
    margin-top: 6px; display: inline-block;
}}

.lila-result {{
    display: grid; grid-template-columns: 1fr 44px 1fr;
    border: 1px solid {BD}; border-radius: 12px;
    overflow: hidden; margin: 1rem 0;
    box-shadow: 0 4px 16px rgba(11,16,38,0.08);
}}
.lila-rs {{ padding: 18px 22px; background: {S1}; }}
.lila-rs.b {{ background: {S2}; }}
.lila-rarrow {{
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, {DARK_BG}, {DARK_S2});
    color: {ACC} !important; font-size: 1.1rem; font-weight: 700;
    font-family: {MO};
}}
.lila-rs-label {{
    font-family: {MO}; font-size: 0.6rem; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: {FA} !important; margin-bottom: 6px;
}}
.lila-rs-crs {{
    font-family: {MO}; font-size: 1.05rem; font-weight: 700;
    color: {P} !important; margin-bottom: 4px;
}}
.lila-rs-name {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.8rem; color: {MU} !important; line-height: 1.45;
}}

.lila-history {{
    border: 1px solid {BD}; border-radius: 10px;
    overflow: hidden; margin-top: 0.6rem;
}}
.lila-hrow {{
    display: grid;
    grid-template-columns: 2.2fr 1fr 1fr 0.8fr 0.4fr;
    border-bottom: 1px solid {BD};
}}
.lila-hrow:last-child {{ border-bottom: none; }}
.lila-hh {{
    font-family: {MO}; font-size: 0.6rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: {FA} !important; padding: 10px 14px; background: {S3};
}}
.lila-hd {{
    padding: 10px 14px; color: {TX} !important;
    background: {S1}; font-size: 0.82rem;
    font-family: 'General Sans', sans-serif !important;
}}
.lila-badge {{
    display: inline-block; font-family: {MO};
    font-size: 0.7rem; font-weight: 600;
    background: {PBG}; color: {P} !important;
    border-radius: 4px; padding: 2px 8px;
    border: 1px solid {PLR};
}}
.lila-badge.n {{
    background: {S3}; color: {MU} !important;
    font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.05em; border: 1px solid {BD2};
    font-weight: 600; font-family: 'General Sans', sans-serif !important;
}}
.lila-ok {{ font-family: {MO}; font-size: 0.78rem; color: {P} !important; font-weight: 700; }}

.lila-footer {{
    margin-top: 3rem; padding-top: 1.2rem;
    border-top: 1px solid {BD};
    display: flex; justify-content: space-between;
    align-items: center; flex-wrap: wrap; gap: 8px;
}}
.lila-footer span {{
    font-family: {MO}; font-size: 0.68rem; color: {FA} !important;
}}
.lila-footer-links {{ display: flex; gap: 18px; }}
.lila-footer-links a {{
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: {FA} !important; text-decoration: none; transition: color 0.15s;
}}
.lila-footer-links a:hover {{ color: {P} !important; }}
</style>
""", unsafe_allow_html=True)

# ── TOP NAV ─────────────────────────────────────────────────
st.markdown(f"""
<div class="lila-topbar">
  <div class="lila-brand">
    <div class="lila-mark">
      <svg width="19" height="19" viewBox="0 0 24 24" fill="none"
           stroke="white" stroke-width="2.2"
           stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10
                 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
    </div>
    <div>
      <div class="lila-brand-name">Lila CRS Converter</div>
      <div class="lila-brand-sub">Geospatial Reprojection Platform</div>
    </div>
  </div>
  <div class="lila-nav-links">
    <a href="https://epsg.io" target="_blank">EPSG.io</a>
    <a href="https://proj.org" target="_blank">PROJ Docs</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ─────────────────────────────────────────────────
left_col, right_col = st.columns([1, 2.4], gap="small")

with left_col:
    st.markdown(f"""
    <div class="lila-left">
      <div class="lila-left-logo">Reproject<br>Spatial Data<br><em>with Precision</em></div>
      <div class="lila-accent-bar"></div>
      <div class="lila-left-desc">
        Convert GeoTIFF, GeoJSON, and Shapefiles to any
        EPSG coordinate reference system — reliably and fast.
      </div>

      <div class="lila-left-stats">
        <div class="lila-left-stat">
          <span class="lila-left-stat-v">25+</span>
          <div class="lila-left-stat-l">EPSG Presets</div>
        </div>
        <div class="lila-left-stat">
          <span class="lila-left-stat-v">3</span>
          <div class="lila-left-stat-l">Output Formats</div>
        </div>
        <div class="lila-left-stat">
          <span class="lila-left-stat-v">Auto</span>
          <div class="lila-left-stat-l">CRS Detection</div>
        </div>
        <div class="lila-left-stat">
          <span class="lila-left-stat-v">∞</span>
          <div class="lila-left-stat-l">File Size</div>
        </div>
      </div>

      <div class="lila-left-feat">
        <div class="lila-feat">
          <div class="lila-feat-dot"></div>
          <div class="lila-feat-text">
            <strong>Auto-detect CRS</strong>
            Reads projection from your file automatically
          </div>
        </div>
        <div class="lila-feat">
          <div class="lila-feat-dot"></div>
          <div class="lila-feat-text">
            <strong>Multiple Formats</strong>
            GeoJSON, GeoPackage, Shapefile output
          </div>
        </div>
        <div class="lila-feat">
          <div class="lila-feat-dot"></div>
          <div class="lila-feat-text">
            <strong>India-Ready EPSG</strong>
            Includes Kalianpur, UTM zones &amp; NSF LCC
          </div>
        </div>
        <div class="lila-feat">
          <div class="lila-feat-dot"></div>
          <div class="lila-feat-text">
            <strong>Batch Upload</strong>
            Upload all Shapefile parts in one step
          </div>
        </div>
      </div>
      <div class="lila-left-footer">
        Powered by PROJ &amp; GDAL<br>
        Lila Geospatial · Athithiyan MR
      </div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="lila-right">', unsafe_allow_html=True)

    # 01 UPLOAD
    st.markdown(f"""
    <div class="lila-section">
      <span class="lila-section-num">01</span>
      <span class="lila-section-name">Upload Files</span>
      <span class="lila-section-line"></span>
    </div>
    <div class="lila-hint">
      For <strong>Shapefiles</strong>, upload all components together:
      <code>.shp</code> &middot; <code>.shx</code> &middot;
      <code>.dbf</code> &middot; <code>.prj</code>
    </div>
    """, unsafe_allow_html=True)

    files = st.file_uploader(
        "upload",
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
            <div class="lila-stat-v p">{total_mb:.1f} MB</div>
            <div class="lila-stat-l">Total Size</div>
          </div>
          <div class="lila-stat">
            <div class="lila-stat-v acc">{exts}</div>
            <div class="lila-stat-l">File Types</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if total_mb > 200:
            st.warning(f"⚠️ {total_mb:.1f} MB — large files may take several minutes.")

    # 02 DETECT & CONFIGURE
    st.markdown(f"""
    <div class="lila-section">
      <span class="lila-section-num">02</span>
      <span class="lila-section-name">Detect &amp; Configure CRS</span>
      <span class="lila-section-line"></span>
    </div>
    """, unsafe_allow_html=True)

    if files:
        btn_col, _ = st.columns([1, 3])
        with btn_col:
            if st.button("🔍  Detect Source CRS"):
                try:
                    with st.spinner("Detecting CRS…"):
                        r = requests.post(
                            f"{API}/detect-crs",
                            files=[("files", f) for f in files],
                            timeout=300,
                        )
                    if r.status_code == 200:
                        st.session_state.detected_crs = r.json().get("crs", "Unknown")
                    else:
                        st.error(r.json().get("detail", r.text))
                except Exception as e:
                    st.error(f"Server error: {e}")

        if st.session_state.detected_crs:
            dname = EPSG_NAMES.get(st.session_state.detected_crs, "Unknown projection")
            st.markdown(f"""
            <div class="lila-detected">
              <span class="dlabel">Detected</span>
              <code>{st.session_state.detected_crs}</code>
              <span class="dname">{dname}</span>
            </div>
            """, unsafe_allow_html=True)

        col_crs, col_fmt = st.columns(2)
        with col_crs:
            preset = st.selectbox("Target CRS", PRESET_CRS)
            if preset == "Custom (enter below)":
                raw = st.text_input("Custom EPSG code", placeholder="e.g. EPSG:7760")
                target_crs = raw.strip().upper() if raw else ""
                if target_crs and not target_crs.startswith("EPSG:"):
                    st.warning("Format must be EPSG:XXXX — e.g. EPSG:4326")
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
                    f'<div style="font-size:0.76rem;color:{FA};margin-top:5px;">'
                    f'Verify at <a href="https://epsg.io/{code}" target="_blank" '
                    f'style="color:{P};font-weight:600;">epsg.io/{code}</a></div>',
                    unsafe_allow_html=True)

        with col_fmt:
            fmt_ui = st.selectbox(
                "Output Format",
                ["GeoJSON (.geojson)", "GeoPackage (.gpkg)", "Shapefile (.zip)"],
            )

        out_fmt = ("geojson" if "GeoJSON" in fmt_ui
                   else "gpkg" if "GeoPackage" in fmt_ui
                   else "shapefile")
        st.session_state.target_crs_final = target_crs
    else:
        st.caption("Upload files in Step 1 to continue.")
        target_crs, out_fmt = "", "geojson"

    # 03 CONVERT
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
        st.caption("Select a target CRS in Step 2 to continue.")
    else:
        if st.button("↺  Convert CRS"):
            try:
                with st.spinner("Reprojecting… this may take a moment."):
                    r = requests.post(
                        f"{API}/convert",
                        files=[("files", f) for f in files],
                        data={"target_crs": target_crs, "output_format": out_fmt},
                        timeout=1800,
                    )
                if r.status_code == 200:
                    st.success("✔ Reprojection complete.")
                    st.session_state.history.insert(0, {
                        "files":  ", ".join(f.name for f in files),
                        "source": st.session_state.detected_crs or "—",
                        "target": target_crs,
                        "format": out_fmt,
                    })
                    ext_map = {
                        "geojson": "reprojected.geojson",
                        "gpkg":    "reprojected.gpkg",
                        "shapefile": "reprojected.zip",
                    }
                    out_name = ("reprojected.tif"
                                if any(f.name.lower().endswith((".tif", ".tiff")) for f in files)
                                else ext_map[out_fmt])

                    src = st.session_state.detected_crs or "—"
                    sn  = EPSG_NAMES.get(src, "Original CRS")
                    tn  = EPSG_NAMES.get(target_crs, "Reprojected CRS")
                    st.markdown(f"""
                    <div class="lila-result">
                      <div class="lila-rs">
                        <div class="lila-rs-label">Source CRS</div>
                        <div class="lila-rs-crs" style="opacity:0.5">{src}</div>
                        <div class="lila-rs-name">{sn}</div>
                      </div>
                      <div class="lila-rarrow">&rarr;</div>
                      <div class="lila-rs b">
                        <div class="lila-rs-label">Target CRS</div>
                        <div class="lila-rs-crs">{target_crs}</div>
                        <div class="lila-rs-name">{tn}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.download_button(
                        "⬇  Download Reprojected File",
                        data=r.content,
                        file_name=out_name,
                        mime="application/octet-stream",
                    )
                else:
                    st.error(r.json().get("detail", r.text))
            except Exception as e:
                st.error(f"Server error: {e}")

    # SESSION HISTORY
    if st.session_state.history:
        st.markdown(f"""
        <div class="lila-section" style="margin-top:2.5rem;">
          <span class="lila-section-num" style="color:{FA};">&#x21BA;</span>
          <span class="lila-section-name">Session History</span>
          <span class="lila-section-line"></span>
        </div>
        """, unsafe_allow_html=True)
        rows = "".join(f"""
        <div class="lila-hrow">
          <div class="lila-hd" style="font-family:'JetBrains Mono',monospace;
               font-size:0.76rem;overflow:hidden;text-overflow:ellipsis;
               white-space:nowrap;">{h['files']}</div>
          <div class="lila-hd"><span class="lila-badge" style="opacity:0.65">{h['source']}</span></div>
          <div class="lila-hd"><span class="lila-badge">{h['target']}</span></div>
          <div class="lila-hd"><span class="lila-badge n">{h['format']}</span></div>
          <div class="lila-hd"><span class="lila-ok">✓</span></div>
        </div>""" for h in st.session_state.history)
        st.markdown(f"""
        <div class="lila-history">
          <div class="lila-hrow">
            <div class="lila-hh">File</div>
            <div class="lila-hh">Source</div>
            <div class="lila-hh">Target</div>
            <div class="lila-hh">Format</div>
            <div class="lila-hh">OK</div>
          </div>{rows}
        </div>
        """, unsafe_allow_html=True)

    # FOOTER
    st.markdown(f"""
    <div class="lila-footer">
      <span>Lila Geospatial · Athithiyan MR · Powered by PROJ &amp; GDAL</span>
      <div class="lila-footer-links">
        <a href="https://epsg.io" target="_blank">EPSG.io</a>
        <a href="https://proj.org" target="_blank">PROJ</a>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
