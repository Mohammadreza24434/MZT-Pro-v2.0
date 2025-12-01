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
    raw = "airguard2025" + expiry
    h = hashlib.md5(raw.encode()).hexdigest().upper()[:12]
    return f"AG25-{h[:4]}-{h[4:8]}-{h[8:]}"

def check_license(code):
    try:
        if not code is None or not code.startswith("AG25-"):
            return False
        clean = code[5:].replace("-", "").upper()
        today = datetime.now().date()
        for d in range(0, 26):  # تا ۲۵ روز آینده چک می‌کنه
            date = today + timedelta(days=d)
            expected = hashlib.md5(("airguard2025" + date.strftime("%Y%m%d")).encode()).hexdigest().upper()[:12]
            if expected == clean and d <= 20:
                return True
        return False
    except:
        return False

# ==================== Professional UI Style (مثل AirGuard Pro) ====================
st.set_page_config(page_title="MZT Pro v2.0", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; padding: 20px; color: white;}
    .title {font-size: 5.5rem; text-align: center; font-weight: 900; background: linear-gradient(90deg, #00ff88, #00f5ff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .subtitle {text-align:center; color:#88ffaa; font-size:2rem; margin-bottom:40px;}
    .license-box {background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); padding: 50px; border-radius: 25px;
                  text-align: center; border: 1px solid rgba(255,255,255,0.2); max-width: 550px; margin: 80px auto;}
    .stButton>button {background: linear-gradient(45deg, #ff6b6b, #ffb142); border: none; border-radius: 50px;
                     height: 70px; font-size: 1.8rem; font-weight: bold; color: white;}
</style>
""", unsafe_allow_html=True)

# ==================== License Check ====================
if 'valid' not in st.session_state:
    st.session_state.valid = False

if not st.session_state.valid:
    st.markdown("<h1 class='title'>MZT Pro v2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Advanced Gaussian Dispersion Modeling • Licensed Version</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='license-box'>", unsafe_allow_html=True)
        st.markdown("### Premium 20-Day License Required")
        code = st.text_input("Enter License Key", type="password", placeholder="AG25-XXXX-XXXX-XXXX")
        if st.button("Activate License"):
            if check_license(code):
                st.session_state.valid = True
                st.success("License Activated Successfully! Enjoy MZT Pro v2.0")
                st.balloons()
                st.rerun()
            else:
                st.error("Invalid or expired license key")

        st.markdown("<br>", unsafe_allow_html=True)
        owner = st.text_input("Owner Access (Developer)", type="password")
        if owner == OWNER_PASSWORD:
            st.success("Welcome back, Developer!")
            if st.button("Generate New 20-Day License"):
                new_key = create_license()
                st.code(new_key, language=None)
                st.info("This key will be valid for 20 days from today.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== Main App (اگر لایسنس معتبر بود) ====================
st.markdown("<h1 class='title'>MZT Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced Gaussian Dispersion Modeling • EPA & Health Threat Zones</p>", unsafe_allow_html=True)

if st.sidebar.button("Logout"):
    st.session_state.valid = False
    st.rerun()

# بقیه کد اصلی MZT Pro (بدون تغییر)
CHEMICALS = {
    "Ammonia (NH3)":           {"molwt":17.03, "IDLH":300,  "ERPG1":25,   "ERPG2":200,  "ERPG3":1000},
    "Chlorine (Cl2)":          {"molwt":70.90, "IDLH":10,   "ERPG1":1,    "ERPG2":3,    "ERPG3":20},
    "Hydrogen Sulfide (H2S)":  {"molwt":34.08, "IDLH":100,  "ERPG1":0.5,  "ERPG2":30,   "ERPG3":100},
    # ... (همه مواد شیمیایی قبلی بدون تغییر)
    "Nitrogen Dioxide":        {"molwt":46.01, "IDLH":20,   "ERPG1":1,    "ERPG2":15,   "ERPG3":30}
}

def advanced_gaussian(Q, u, H, stability, x_max=60):
    x = np.linspace(10, x_max*1000, 1200)
    y = np.linspace(-x_max*1000, x_max*1000, 1200)
    X, Y = np.meshgrid(x, y)
    sy = {'A':0.22,'B':0.16,'C':0.11,'D':0.08,'E':0.06,'F':0.04}.get(stability,0.08) * X**0.894
    sz = {'A':0.20,'B':0.12,'C':0.08,'D':0.06,'E':0.03,'F':0.02}.get(stability,0.06) * X**0.894
    C = (Q/(2*np.pi*u*sy*sz)) * np.exp(-0.5*(Y/sy)**2) * (np.exp(-0.5*((0-H)/sz)**2) + np.exp(-0.5*((0+H)/sz)**2))
    return X/1000, Y/1000, np.nan_to_num(C, nan=0.0)

with st.sidebar:
    st.header("Scenario Parameters")
    chem_name = st.selectbox("Select Chemical", sorted(CHEMICALS.keys()))
    chem = CHEMICALS[chem_name]
    molwt = chem["molwt"]
    Q = st.slider("Release Rate (g/s)", 10, 50000, 5000, 500)
    u = st.slider("Wind Speed (m/s)", 0.5, 25.0, 4.0, 0.1)
    temp_c = st.slider("Temperature (°C)", -10, 50, 25)
    H = st.slider("Release Height (m)", 0.0, 150.0, 5.0, 0.5)
    stability = st.selectbox("Stability Class", ["A","B","C","D","E","F"], index=3)
    view_mode = st.radio("Display Mode", ["Filled Contours", "Line Contours"])

X_km, Y_km, C_gm3 = advanced_gaussian(Q, u, H, stability)
C_ppm = C_gm3 * 24.45 / molwt * (298.15 / (temp_c + 273.15))

fig, ax = plt.subplots(figsize=(18, 12))

if view_mode == "Filled Contours":
    cont = ax.contourf(X_km, Y_km, C_ppm, levels=80, cmap="inferno", norm=LogNorm(vmin=1e-3, vmax=C_ppm.max()), alpha=0.92)
    plt.colorbar(cont, ax=ax, shrink=0.75, pad=0.02, label="Concentration (ppm)")
else:
    levels = np.logspace(np.log10(max(0.01, C_ppm.max()*1e-6)), np.log10(C_ppm.max()), 25)
    ax.contour(X_km, Y_km, C_ppm, levels=levels, colors='#00ffff', linewidths=1.6, alpha=0.95)

zones = [("ERPG3","red",6), ("ERPG2","orange",5), ("ERPG1","yellow",4), ("IDLH","crimson",5), ("LEL","magenta",6)]
threat_info = []

for key, color, width in zones:
    if key in chem:
        level = chem[key] * (10000 if key == "LEL" else 1)
        if C_ppm.max() >= level * 0.4:
            ax.contour(X_km, Y_km, C_ppm, levels=[level], colors=color, linewidths=width)
            unit = "%" if key == "LEL" else "ppm"
            threat_info.append(f"<span style='color:{color};font-weight:bold'>{key}</span>: {chem[key]:.2f} {unit}")

ax.set_title(f"MZT Pro v2.0 — {chem_name}\nQ: {Q:,} g/s | u: {u} m/s | H: {H} m | Class: {stability}", 
             fontsize=20, color="#00ffff", pad=30, weight="bold")
ax.set_xlabel("Downwind Distance (km)", fontsize=14, color="white")
ax.set_ylabel("Crosswind Distance (km)", fontsize=14, color="white")
ax.grid(True, alpha=0.2, color="#333333")
ax.set_facecolor("#0d1117")
fig.patch.set_facecolor("#0a0e17")
ax.tick_params(colors='white')
ax.set_xlim(0, 50)
ax.set_ylim(-25, 25)
ax.axis("equal")

st.pyplot(fig)

if threat_info:
    st.markdown("### Threat Zones")
    st.markdown("<div style='background:#111;padding:20px;border-radius:12px;text-align:center;font-size:18px'>" +
                "  |  ".join(threat_info) + "</div>", unsafe_allow_html=True)

st.markdown("### Maximum Threat Distances (km)")
cols = st.columns(5)
for col, name, color in zip(cols, ["ERPG-3", "ERPG-2", "ERPG-1", "IDLH", "LEL"], ["red", "orange", "yellow", "crimson", "magenta"]):
    key = name.replace("-", "") if "ERPG" in name else name
    if key in chem:
        level = chem[key] * (10000 if key == "LEL" else 1)
        dists = X_km[0][np.where(np.max(C_ppm, axis=0) >= level)]
        dist = dists[-1] if len(dists)>0 else 0.0
        col.markdown(f"<h4 style='color:{color}'>{name}</h4><h1 style='color:{color}'>{dist:.2f}</h1>", unsafe_allow_html=True)
    else:
        col.markdown(f"<h4 style='color:gray'>{name}</h4><h2>N/A</h2>", unsafe_allow_html=True)

buf = BytesIO()
fig.savefig(buf, format="png", dpi=500, bbox_inches="tight", facecolor="#0a0e17")
buf.seek(0)
st.download_button("Download Map (500 DPI PNG)", buf, f"MZT_Pro_v2_{chem_name.replace(' ', '_')}.png", "image/png")

st.caption("MZT Pro v2.0 © 2025 • Licensed Version • Advanced Gaussian Plume Modeling")
