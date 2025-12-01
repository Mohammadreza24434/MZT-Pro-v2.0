import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from io import BytesIO
from datetime import datetime, timedelta
import hashlib

# ==================== License System (20-Day Premium) ====================
OWNER_PASSWORD = "24434"

def create_license():
    expiry = (datetime.now() + timedelta(days=20)).strftime("%Y%m%d")
    raw = "mztpro2025" + expiry  # تغییر دادم که با AirGuard تداخل نداشته باشه
    h = hashlib.md5(raw.encode()).hexdigest().upper()[:12]
    return f"MZ25-{h[:4]}-{h[4:8]}-{h[8:]}"

def check_license(code):
    if not code or not code.startswith("MZ25-"):
        return False
    clean = code[5:].replace("-", "").upper()
    today = datetime.now().date()
    for d in range(0, 26):
        check_date = today + timedelta(days=d)
        expected = hashlib.md5(("mztpro2025" + check_date.strftime("%Y%m%d")).encode()).hexdigest().upper()[:12]
        if expected == clean and d <= 20:
            return True
    return False

# ==================== Full Chemicals Database (۴۲ ماده خطرناک) ====================
CHEMICALS = {
    "Ammonia (NH3)":           {"molwt":17.03, "IDLH":300,   "ERPG1":25,   "ERPG2":200,   "ERPG3":1000},
    "Chlorine (Cl2)":          {"molwt":70.90, "IDLH":10,    "ERPG1":1,    "ERPG2":3,     "ERPG3":20},
    "Hydrogen Sulfide (H2S)":  {"molwt":34.08, "IDLH":100,   "ERPG1":0.5,  "ERPG2":30,    "ERPG3":100},
    "Sulfur Dioxide (SO2)":    {"molwt":64.06, "IDLH":100,   "ERPG1":0.3,  "ERPG2":15,    "ERPG3":75},
    "Hydrogen Fluoride (HF)":  {"molwt":20.01, "IDLH":30,    "ERPG1":5,    "ERPG2":20,    "ERPG3":50},
    "Hydrogen Chloride (HCl)": {"molwt":36.46, "IDLH":50,    "ERPG1":3,    "ERPG2":20,    "ERPG3":150},
    "Phosgene":                {"molwt":98.92, "IDLH":2,     "ERPG1":0.2,  "ERPG2":0.5,   "ERPG3":1},
    "Methyl Isocyanate":       {"molwt":57.05, "IDLH":3,     "ERPG1":0.2,  "ERPG2":1,     "ERPG3":5},
    "Hydrogen Cyanide (HCN)":  {"molwt":27.03, "IDLH":50,    "ERPG1":10,   "ERPG2":20,    "ERPG3":50},
    "Bromine (Br2)":           {"molwt":159.8, "IDLH":3,     "ERPG1":0.1,  "ERPG2":0.5,   "ERPG3":5},
    "Acrylonitrile":           {"molwt":53.06, "IDLH":85,    "ERPG1":10,   "ERPG2":35,    "ERPG3":75},
    "Ethylene Oxide":          {"molwt":44.05, "IDLH":800,   "ERPG1":5,    "ERPG2":50,    "ERPG3":500},
    "Formaldehyde":            {"molwt":30.03,  "IDLH":20,    "ERPG1":1,    "ERPG2":10,    "ERPG3":25},
    "Carbon Monoxide (CO)":    {"molwt":28.01, "IDLH":1200,  "ERPG1":200,  "ERPG2":350,   "ERPG3":500},
    "Methanol":                {"molwt":32.04, "IDLH":6000,  "ERPG1":200,  "ERPG2":1000,  "ERPG3":5000},
    "Benzene":                 {"molwt":78.11, "IDLH":500,   "ERPG1":50,   "ERPG2":150,   "ERPG3":1000},
    "Toluene":                 {"molwt":92.14, "IDLH":500,   "ERPG1":50,   "ERPG2":300,   "ERPG3":1000},
    "Phosphine (PH3)":         {"molwt":34.00, "IDLH":50,    "ERPG1":0.3,  "ERPG2":2,     "ERPG3":10},
    "Arsine (AsH3)":           {"molwt":77.95, "IDLH":3},
    "Fluorine (F2)":           {"molwt":38.00, "IDLH":25},
    "Nitrogen Dioxide (NO2)":  {"molwt":46.01, "IDLH":20,    "ERPG1":1,    "ERPG2":15,    "ERPG3":30},
    "Ozone (O3)":              {"molwt":48.00, "IDLH":5},
    "Acrolein":                {"molwt":56.06, "IDLH":2,     "ERPG1":0.1,  "ERPG2":0.5,   "ERPG3":3},
    "Vinyl Chloride":          {"molwt":62.50, "IDLH":1000,  "ERPG1":10,   "ERPG2":50,    "ERPG3":500},
    "Hydrazine":               {"molwt":32.05, "IDLH":50,    "ERPG1":0.5,   "ERPG2":3,     "ERPG3":30},
    "Carbon Disulfide":        {"molwt":76.14, "IDLH":500,   "ERPG1":10,   "ERPG2":50,    "ERPG3":200},
    "Nitric Acid (HNO3)":      {"molwt":63.01, "IDLH":25},
    "Sulfuric Acid (H2SO4)":   {"molwt":98.08, "IDLH":15},
    "Oleum":                   {"molwt":80.06, "IDLH":10},
    "Aniline":                 {"molwt":93.13, "IDLH":100},
    "Methane":                 {"molwt":16.04, "LEL":5.0},
    "Propane":                 {"molwt":44.10, "LEL":2.1},
    "Butane":                  {"molwt":58.12, "LEL":1.8},
    "Hydrogen":                {"molwt":2.02,  "LEL":4.0},
    "LPG":                     {"molwt":48.0,  "LEL":2.0},
    "LNG (Methane)":           {"molwt":17.0,  "LEL":5.0},
    "Acetone":                 {"molwt":58.08, "LEL":2.5},
    "Ethanol":                {"molwt":46.07, "IDLH":3300, "ERPG1":100,  "ERPG2":500,   "ERPG3":2500},
    "Styrene":                 {"molwt":104.15,"IDLH":700,   "ERPG1":20,   "ERPG2":100,   "ERPG3":500},
    "Chloroform":              {"molwt":119.38,"IDLH":500},
    "Dichloromethane":         {"molwt":84.93, "IDLH":2300},
}

# ==================== UI & License ====================
st.set_page_config(page_title="MZT Pro v2.0", page_icon="Warning", layout="wide")

st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; padding: 20px; color: white;}
    .title {font-size: 5.5rem; text-align: center; font-weight: 900; background: linear-gradient(90deg, #ff6b6b, #ff4757);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .license-box {background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); padding: 50px; border-radius: 25px;
                  text-align: center; border: 1px solid rgba(255,255,255,0.2); max-width: 600px; margin: 60px auto;}
    .stButton>button {background: linear-gradient(45deg, #ff4757, #ffa502); border: none; border-radius: 50px;
                     height: 70px; font-size: 1.8rem; font-weight: bold; color: white;}
</style>
""", unsafe_allow_html=True)

if 'valid' not in st.session_state:
    st.session_state.valid = False

if not st.session_state.valid:
    st.markdown("<h1 class='title'>MZT Pro v2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ff6b6b; font-size:2.2rem;'>Advanced Chemical Release Modeling • 42 Hazardous Substances</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='license-box'>", unsafe_allow_html=True)
        st.markdown("### Premium 20-Day License Required")
        code = st.text_input("Enter License Key", type="password", placeholder="MZ25-XXXX-XXXX-XXXX", key="lic")
        
        if st.button("Activate License", type="primary"):
            if check_license(code):
                st.session_state.valid = True
                st.success("MZT Pro v2.0 Activated Successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("Invalid or expired license key")

        st.markdown("<br>", unsafe_allow_html=True)
        owner = st.text_input("Owner Access", type="password", key="owner")
        if owner == OWNER_PASSWORD:
            st.success("Welcome back, Developer!")
            if st.button("Generate New License Key"):
                key = create_license()
                st.code(key, language=None)
                st.info("Valid for 20 days from today • Format: MZ25-XXXX-XXXX-XXXX")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== Main App ====================
st.markdown("<h1 class='title'>MZT Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ff4757; font-size:2rem;'>Professional Gaussian Dispersion Modeling • 42 Chemicals</p>", unsafe_allow_html=True)

if st.sidebar.button("Logout"):
    st.session_state.valid = False
    st.rerun()

def advanced_gaussian(Q, u, H, stability, x_max=60):
    x = np.linspace(10, x_max*1000, 1200)
    y = np.linspace(-x_max*1000, x_max*1000, 1200)
    X, Y = np.meshgrid(x, y)
    sy = {'A':0.22,'B':0.16,'C':0.11,'D':0.08,'E':0.06,'F':0.04}.get(stability,0.08) * X**0.894
    sz = {'A':0.20,'B':0.12,'C':0.08,'D':0.06,'E':0.03,'F':0.02}.get(stability,0.06) * X**0.894
    C = (Q/(2*np.pi*u*sy*sz)) * np.exp(-0.5*(Y/sy)**2) * (np.exp(-0.5*((0-H)/sz)**2) + np.exp(-0.5*((0+H)/sz)**2))
    return X/1000, Y/1000, np.nan_to_num(C, nan=0.0)

with st.sidebar:
    st.header("Release Scenario")
    chem_name = st.selectbox("Chemical", sorted(CHEMICALS.keys()))
    chem = CHEMICALS[chem_name]
    molwt = chem["molwt"]
    Q = st.slider("Release Rate (g/s)", 10, 100000, 10000, 500)
    u = st.slider("Wind Speed (m/s)", 0.5, 30.0, 5.0, 0.1)
    temp_c = st.slider("Temperature (°C)", -20, 60, 25)
    H = st.slider("Release Height (m)", 0.0, 200.0, 10.0, 1.0)
    stability = st.selectbox("Pasquill Stability", ["A","B","C","D","E","F"], index=3)
    view_mode = st.radio("View", ["Filled Contours", "Line Contours"])

X_km, Y_km, C_gm3 = advanced_gaussian(Q, u, H, stability)
C_ppm = C_gm3 * 24.45 / molwt * (298.15 / (temp_c + 273.15))

fig, ax = plt.subplots(figsize=(18, 12))

if view_mode == "Filled Contours":
    cont = ax.contourf(X_km, Y_km, C_ppm, levels=100, cmap="inferno", norm=LogNorm(vmin=1e-4, vmax=C_ppm.max()))
    plt.colorbar(cont, ax=ax, shrink=0.8, label="Concentration (ppm)")
else:
    levels = np.logspace(-4, np.log10(C_ppm.max()), 30)
    ax.contour(X_km, Y_km, C_ppm, levels=levels, colors='#00ffff', linewidths=1.5)

# Threat Zones
zones = [("ERPG3","red",7), ("ERPG2","orange",6), ("ERPG1","yellow",5), ("IDLH","crimson",6), ("LEL","magenta",7)]
threat_info = []
for key, color, width in zones:
    if key in chem:
        level = chem[key] * (10000 if key == "LEL" else 1)
        if C_ppm.max() >= level * 0.3:
            ax.contour(X_km, Y_km, C_ppm, levels=[level], colors=color, linewidths=width)
            unit = "% LEL" if key == "LEL" else "ppm"
            threat_info.append(f"<span style='color:{color};font-weight:bold'>{key}</span>: {chem[key]} {unit}")

ax.set_title(f"MZT Pro v2.0 — {chem_name}\nRelease: {Q:,} g/s • Wind: {u} m/s • Height: {H} m • Class {stability}", 
             fontsize=22, color="#ff4757", pad=30, weight="bold")
ax.set_xlabel("Downwind Distance (km)", fontsize=14, color="white")
ax.set_ylabel("Crosswind Distance (km)", fontsize=14, color="white")
ax.grid(True, alpha=0.3)
ax.set_facecolor("#0a0e17")
fig.patch.set_facecolor("#0a0e17")
ax.tick_params(colors='white')
ax.set_xlim(0, 50)
ax.set_ylim(-30, 30)
ax.axis("equal")

st.pyplot(fig)

if threat_info:
    st.markdown("### Active Threat Zones")
    st.markdown("<div style='background:#200; padding:20px; border-radius:15px; text-align:center; font-size:19px'>" +
                "  |  ".join(threat_info) + "</div>", unsafe_allow_html=True)

# Download
buf = BytesIO()
fig.savefig(buf, format="png", dpi=600, bbox_inches="tight", facecolor="#0a0e17")
buf.seek(0)
st.download_button("Download High-Res Map (600 DPI)", buf, f"MZT_Pro_{chem_name.replace(' ', '_')}.png", "image/png")

st.caption("MZT Pro v2.0 © 2025 • Premium Licensed • 42 Hazardous Chemicals • Real-Time Gaussian Modeling")
