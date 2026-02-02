import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from utils import img_to_base64
import streamlit as st
from utils import load_css

load_css()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NEXUS AI | Forest Smart Birdhouse",
    layout="wide",
    page_icon="🌲"
)

# ============================================================
# LANGUAGES
# ============================================================
LANGS = {
    "English": {
        "title": "🧠 NEXUS AI Hub",
        "subtitle": "Forest Smart Birdhouse – Ground Truth Layer",
        "menu": "Select Chapter",
        "back": "⬅️ Back to AI Hub",
        "dir": "ltr"
    },
    "Deutsch": {
        "title": "🧠 NEXUS KI-Zentrum",
        "subtitle": "Forest Smart Birdhouse – Ground-Truth-Ebene",
        "menu": "Kapitel auswählen",
        "back": "⬅️ Zurück zum KI-Hub",
        "dir": "ltr"
    },
    "العربية": {
        "title": "🧠 مركز نكسوس للذكاء الاصطناعي",
        "subtitle": "بيت الطيور الذكي – طبقة التحقق الأرضية",
        "menu": "اختر القسم",
        "back": "⬅️ العودة إلى مركز الذكاء الاصطناعي",
        "dir": "rtl"
    }
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    lang = st.selectbox("🌐 Language", list(LANGS.keys()))
    T = LANGS[lang]

    menu = st.radio(
    T["menu"],
    [
        "1. Concept Overview",
        "2. Internal Engineering",
        "3. Network & Connectivity",
        "4. Power System",
        "5. Fleet Health",
        "6. QR & Maintenance",
        "7. Cost Analysis (BOM)"
    ]
)

    st.divider()
    if st.button(T["back"], use_container_width=True):
        st.switch_page("pages/1_AI_Hub.py")


# ============================================================
# CSS (تحسين واضح + إزالة الأزرق الغامق + قراءة أفضل)
# ============================================================
# CSS المحدث (نمط الأورنج + نصوص سوداء + عناوين واضحة)
# ============================================================
st.markdown(f"""
<style>
/* ====== GLOBAL ====== */
.main {{
    direction:{T['dir']};
    background:#EAF4EC; /* خلفية فاتحة لتناسب العناوين السوداء */
}}

/* العناوين - جعلها سوداء بخط عريض وجذاب */
.section {{
    margin:2rem 0 1rem 0;
    padding-bottom:10px;
    border-bottom:3px solid #FF8C00; /* خط برتقالي تحت العنوان */
    font-size:1.8rem;
    font-weight: 800;
    color:#000000 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* ====== الكروت بألوانك الأصلية (الشفافة) ====== */

/* كرت الحالة (Status) */
.status-card {{
  background: rgba(251, 146, 60, 0.15); 
  backdrop-filter: blur(12px);
  padding: 22px;
  border-radius: 16px;
  border: 1px solid #f97316;
  margin-top: 14px;
  color: #000000 !important; /* الكتابة سوداء */
}}

/* كرت المؤشرات (KPI) */
.kpi-card {{
  background: rgba(234, 88, 12, 0.1); 
  border: 1px solid rgba(251, 146, 60, 0.4);
  border-radius: 16px;
  padding: 16px 18px;
  color: #000000 !important; /* الكتابة سوداء */
}}

/* الصناديق التي كانت تسمى box و system - قمت بتعديلها لتأخذ نفس طابعك الأصلي */
.box, .system {{
    background: rgba(251, 146, 60, 0.15); 
    backdrop-filter: blur(12px);
    padding:22px;
    border-radius:16px;
    border:1px solid #f97316;
    color:#000000 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

/* التأكد من أن أي نص داخل الكروت هو أسود */
.status-card *, .kpi-card *, .box *, .system * {{
    color: #000000 !important;
}}

/* التنبيهات */
.alert {{
    animation:pulse 1.5s infinite;
    border:2px solid #dc2626;
    background:#fee2e2;
    color:#7f1d1d;
    padding:14px 16px;
    border-radius:12px;
    font-weight:700;
}}

@keyframes pulse {{
    0% {{opacity:1}}
    50% {{opacity:.6}}
    100% {{opacity:1}}
}}

/* شرائح القواعد (rule-chips) داخل الكروت */
.rule-chip {{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:.8rem;
    padding:.6rem .9rem;
    border-radius:12px;
    border:1px solid rgba(0,0,0,0.1);
    background: rgba(255,255,255,0.4); /* خلفية بيضاء شفافة لتظهر فوق الأورنج */
    margin:.4rem 0;
    color:#000000 !important;
}}

.rule-chip.on {{
    border:2px solid #000000;
    background: rgba(255,255,255,0.6);
}}

.rule-title {{
    font-weight:900;
    color: #000000 !important;
}}

.rule-sub {{
    font-size:.9rem;
    color:#000000 !important;
    opacity: 0.8;
}}

.rule-weight {{
    font-weight:900;
    color:#000000 !important;
}}

.small-note {{
    color:#000000;
    font-size:.92rem;
    opacity: 0.7;
}}

/* تحسين أي نصوص ماركداون إضافية لتكون سوداء */
div[data-testid="stMarkdownContainer"] p {{
    color: #000000 !important;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.title(T["title"])
st.caption(T["subtitle"])

# assets path
ASSETS = "assets/"

# ============================================================
# SESSION STATE (كما هو + إصلاح rerun)
# ============================================================
if "fire_sim" not in st.session_state:
    st.session_state.fire_sim = False

if "play_sound" not in st.session_state:
    st.session_state.play_sound = False

# ============================================================
# LIVE DATA (SIMULATED) — كما هو
# ============================================================
if st.session_state.fire_sim:
    live_temp = 65
    live_hum = 7
    live_smoke = 820
    battery = 42
else:
    live_temp = 36
    live_hum = 18
    live_smoke = 240
    battery = 78

# ============================================================
# AUDIO ALERT (ONLY WHEN FIRE) — كما هو
# ============================================================
if st.session_state.play_sound:
    st.audio("https://www.soundjay.com/misc/sounds/alarm-clock-01.mp3")
    st.session_state.play_sound = False

# ============================================================
# SENSOR CONFIRMATION (قواعد مبسطة مأخوذة من صفحة FireSense)
# ============================================================
RULES = [
    {"name": "PM2.5 Spike", "desc": "PM2.5 > 50 µg/m³", "weight": 0.45, "on": lambda pm25, t, rh: pm25 > 50},
    {"name": "Low Humidity", "desc": "RH < 30%", "weight": 0.35, "on": lambda pm25, t, rh: rh < 30},
    {"name": "High Temperature", "desc": "Temp > 30°C", "weight": 0.25, "on": lambda pm25, t, rh: t > 30},
]

def compute_sensor_event_score(pm25: float, temp_c: float, rh: float, enable_false_alarm_filter: bool = True, rh_safe: float = 55.0):
    """
    Transparent score: sum(weights of fired rules), clipped to 1.0
    False-alarm filter: if RH high, ignore PM spike contribution.
    """
    fired = []
    score = 0.0

    # Apply false-alarm filter (optional)
    pm25_for_rules = pm25
    false_alarm_active = False
    if enable_false_alarm_filter and rh >= rh_safe:
        pm25_for_rules = min(pm25, 50)  # keep at/below threshold
        false_alarm_active = True

    for r in RULES:
        is_on = bool(r["on"](pm25_for_rules, temp_c, rh))
        fired.append((r, is_on))
        if is_on:
            score += float(r["weight"])

    return float(min(score, 1.0)), fired, false_alarm_active

def battery_health_percent(pct: float):
    if pct >= 70:
        return "Good", "🟢"
    if pct >= 40:
        return "Medium", "🟡"
    return "Low", "🔴"

def link_health_from_sim(pm25: float, rh: float):
    # Simple deterministic link state for demo (you can replace with RSSI later)
    # If fire sim (very high pm25) assume signal can be noisy
    if pm25 >= 700:
        return "Medium", "🟡"
    return "Strong", "🟢"

# ============================================================
# 1. CONCEPT
# ============================================================
if menu == "1. Concept Overview":
    st.markdown('<div class="section">🌲 Ground Truth Layer</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        # تصغير الصور (بدون use_column_width)
        st.image(f"{ASSETS}Hero Image Prompt.PNG", width=520)

    with c2:
        st.markdown("""
        <div class="box">
        The <b>Forest Smart Birdhouse</b> acts as a <b>Ground Truth Layer</b>,
        validating satellite-based AI predictions with real-time field data.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 2. ENGINEERING (إضافة: جدول حساسات + صورة cutaway)
# ============================================================
elif menu == "2. Internal Engineering":
    st.markdown('<div class="section">⚙️ Internal Engineering</div>', unsafe_allow_html=True)

    # --- NEW: Sensor Table (Decision-oriented) ---
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.markdown("### 🧾 Sensor Stack (Node Specification)")
    sensor_table = pd.DataFrame([
        {"Module": "ESP32 + LoRa", "Measures": "Compute + Long-range link", "Role": "Edge processing + uplink", "Why it matters for AI": "Reliable data delivery + low power"},
        {"Module": "BME280", "Measures": "Temp / RH / Pressure", "Role": "Fuel dryness context", "Why it matters for AI": "Baseline risk calibration"},
        {"Module": "PMS5003", "Measures": "PM2.5", "Role": "Early smoke particles", "Why it matters for AI": "Detect ignition before flames"},
        {"Module": "CCS811", "Measures": "VOC / Air quality", "Role": "Gas confirmation", "Why it matters for AI": "Reduce false alarms"},
        {"Module": "Heating Resistor", "Measures": "Internal stability", "Role": "Anti-condensation / anti-freeze", "Why it matters for AI": "Stable sensors = stable decision"},
        {"Module": "Power (Solar + Battery)", "Measures": "Energy autonomy", "Role": "Off-grid operation", "Why it matters for AI": "Continuous monitoring"},
        {"Module": "IP65 Enclosure", "Measures": "Protection + airflow", "Role": "Outdoor survivability", "Why it matters for AI": "Long-term reliability"},
        {"Module": "LoRa Antenna", "Measures": "Link gain", "Role": "Range in forest", "Why it matters for AI": "Network scalability"},
    ])
    st.dataframe(sensor_table, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- NEW: Internal Cutaway Image (from your provided image) ---
    st.markdown('<div class="section">🧩 Technical Cutaway & Airflow</div>', unsafe_allow_html=True)
    ccut1, ccut2 = st.columns([1.2, 1])
    with ccut1:
        st.image(f"{ASSETS}Internal Cutaway Prompt.png", width=560, caption="Two-Chamber Internal Design + Airflow")
    with ccut2:
        st.markdown("""
        <div class="box">
        <b>Two-Chamber Architecture</b><br><br>
        1) <b>Sealed chamber</b> protects MCU + battery.<br>
        2) <b>Ventilated chamber</b> ensures accurate smoke & gas readings via controlled airflow.<br><br>
        <b>Why it matters:</b> Stable airflow + protected electronics → fewer false readings and higher AI trust.
        </div>
        """, unsafe_allow_html=True)

    # --- existing expanders (kept) ---
    with st.expander("🔍 Sensors Module"):
        st.write("CO, CO₂, NO₂, PM2.5 – early combustion indicators.")

    with st.expander("🧠 Processing Unit (Edge AI)"):
        st.write("On-device anomaly detection reduces bandwidth and energy usage.")

    with st.expander("🏠 Enclosure & Materials"):
        st.write("Sustainable wood housing with optimized ventilation and low carbon footprint.")

    st.markdown('<div class="section">📡 Live Sensor Feed</div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2)

    with g1:
        fig_temp = go.Figure(go.Indicator(
            mode="gauge+number",
            value=live_temp,
            title={"text": "Temperature °C"},
            gauge={"axis": {"range": [0, 80]}, "bar": {"color": "orange"}}
        ))
        st.plotly_chart(fig_temp, use_container_width=True)

    with g2:
        fig_smoke = go.Figure(go.Indicator(
            mode="gauge+number",
            value=live_smoke,
            title={"text": "Smoke PM2.5"},
            gauge={"axis": {"range": [0, 1000]}, "bar": {"color": "red"}}
        ))
        st.plotly_chart(fig_smoke, use_container_width=True)

    if live_smoke > 600:
        st.markdown('<div class="alert">🔥 CRITICAL SMOKE DETECTED – EARLY WARNING ACTIVE</div>', unsafe_allow_html=True)

    if st.button("🔥 Simulate Fire"):
        st.session_state.fire_sim = True
        st.session_state.play_sound = True
        st.rerun()

    st.markdown("""
    <div class="system">
    <b>Ground Truth Impact</b><br>
    Satellite-only → Moderate Risk<br>
    With Birdhouse → <b>HIGH RISK (Override)</b>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔗 Open AI Hub with Birdhouse Data", use_container_width=True):
        st.session_state["field_data"] = {
            "t": live_temp,
            "h": live_hum,
            "w": 20,
            "source": "Birdhouse Node #01"
        }
        st.switch_page("pages/1_AI_Hub.py")

# ============================================================
# 3. NETWORK (kept + images smaller)
# ============================================================
elif menu == "3. Network & Connectivity":
    st.markdown('<div class="section">📡 Network & Coverage</div>', unsafe_allow_html=True)
    st.image(f"{ASSETS}Network Overview Prompt.png", width=650)
    st.image(f"{ASSETS}forest_lora_gateway_node.png", width=420)
    st.markdown("""
<div class="box">
<b>Distributed Communication Layer</b><br><br>
Wildfires are spatial phenomena that evolve across large landscapes.
For this reason, Birdhouse nodes operate as a distributed sensor network.

LoRa communication enables long-range, low-power transmission even in remote forests.
When connectivity is temporarily unavailable, nodes store data locally and
synchronize automatically once the link is restored, ensuring system resilience.
</div>
""", unsafe_allow_html=True)

     
# ============================================================
# 4. POWER SYSTEM (kept + add battery chart as before)
# ============================================================
elif menu == "4. Power System":
    st.markdown('<div class="section">🔋 Power & Energy</div>', unsafe_allow_html=True)

    hours = np.arange(24)
    energy = np.clip(50 + 30*np.sin((hours-6)/24*2*np.pi), 10, 100)

    st.area_chart(pd.DataFrame({"Battery %": energy}))
    st.metric("Current Battery Level", f"{battery}%")
    st.image(f"{ASSETS}Solar Power Detail.png", width=420)
    st.markdown("""
<div class="box">
<b>Energy Autonomy Design</b><br><br>
The Birdhouse power system is optimized for long-term off-grid operation.
A hybrid solar–battery architecture combined with sleep–wake cycles
minimizes energy consumption while ensuring availability during critical events.

This allows continuous operation for months or years without maintenance,
which is essential for large-scale forest deployment.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 5. FLEET HEALTH + MAP (kept)
# ============================================================
elif menu == "5. Fleet Health":
    st.markdown('<div class="section">📍 Fleet Health Status</div>', unsafe_allow_html=True)

    fleet = pd.DataFrame({
        "Node": ["#01", "#02", "#03"],
        "Battery": ["78%", "41%", "Offline"],
        "Status": ["OK", "Warning", "Offline"]
    })
    st.table(fleet)
    st.markdown("""
<div class="box">
<b>Spatial Maintenance Awareness</b><br><br>
The map provides geographic context for the fleet, allowing maintenance teams
to efficiently locate nodes and plan field interventions.
</div>
""", unsafe_allow_html=True)


    st.markdown("### Node Location Map")
    map_df = pd.DataFrame({
        "lat": [50.94],
        "lon": [6.96],
        "node": ["Birdhouse Node #01"]
    })
    st.map(map_df, zoom=11)
    st.markdown("""
<div class="box">
<b>Operational Fleet Monitoring</b><br><br>
This table provides a real-time overview of the health of all deployed Birdhouse nodes.
It enables operators to identify degraded, offline, or low-power nodes
before data quality is affected.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 6) QR Code & Maintenance Intelligence (Birdhouse IQ)
# ============================================================
elif menu == "6. QR & Maintenance":

    st.markdown(
        '<div class="section">🧠 Node IQ – QR Code & Maintenance Intelligence</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        st.image(
            f"{ASSETS}birdhouse_qr_maintenance_detail.png",
            caption="QR Code – Physical Identity of the Birdhouse Node",
            width=420
        )

    with c2:
        st.markdown("""
<div class="box">
<b>Academic Context</b><br><br>
This ground-truth layer bridges the gap between large-scale satellite intelligence
and local physical reality. By sensing temperature, humidity, and airborne particles
directly inside the forest, the system confirms AI predictions with empirical evidence.

This significantly reduces false alarms and transforms NEXUS into a
<b>verified decision-support system</b>.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 7. BOM (kept + add BOM infographic image you provided)
# ============================================================
elif menu == "7. Cost Analysis (BOM)":
    st.markdown('<div class="section">💰 Bill of Materials</div>', unsafe_allow_html=True)

    # NEW: BOM infographic at top
    st.image(f"{ASSETS}bom_cost_infographic.png", width=420, caption="BOM & Cost Estimate (per node)")
    st.markdown("""
<div class="box">
<b>Economic Scalability</b><br><br>
The Bill of Materials demonstrates that each Birdhouse node can be produced
at low cost while maintaining high sensing quality.

This cost structure enables large-scale deployment, making the NEXUS system
economically viable for regional and national wildfire monitoring programs.
</div>
""", unsafe_allow_html=True)

    bom = pd.DataFrame({
        "Component": ["ESP32 + LoRa", "Gas & Smoke Sensors", "Battery + Solar", "Enclosure"],
        "Cost (€)": [15, 15, 14, 10]
    })
    st.table(bom)
    st.metric("Estimated Unit Cost", "≈ 60 €")

# ============================================================
# ADDITION: Sensor Confirmation (from FireSense) inside Live Sensors & Alerts
# (بدون تغيير أقسامك: نضيفه كقسم إضافي يظهر ضمن Engineering لما يكون فيه Live)
# ============================================================
if menu == "2. Internal Engineering":
    st.markdown('<div class="section">✅ Sensor Confirmation Logic (Explainable)</div>', unsafe_allow_html=True)

    enable_false_alarm_filter = True
    rh_safe = 55.0

    sensor_score, fired, false_alarm_active = compute_sensor_event_score(
        pm25=float(live_smoke),
        temp_c=float(live_temp),
        rh=float(live_hum),
        enable_false_alarm_filter=enable_false_alarm_filter,
        rh_safe=rh_safe
    )

    # health cards
    b_state, b_icon = battery_health_percent(float(battery))
    l_state, l_icon = link_health_from_sim(float(live_smoke), float(live_hum))

    h1, h2, h3 = st.columns([1, 1, 1.2])
    h1.metric("Battery Health", f"{b_icon} {b_state}")
    h2.metric("Link Quality", f"{l_icon} {l_state}")
    h3.metric("Sensor Event Score", f"{sensor_score:.2f} / 1.00")

    st.progress(int(sensor_score * 100))
    st.caption("This score is based on transparent rules (no black box).")

    # rules list
    for rule, on in fired:
        cls = "rule-chip on" if on else "rule-chip"
        st.markdown(
            f"""
<div class="{cls}">
  <div>
    <div class="rule-title">{rule['name']}</div>
    <div class="rule-sub">{rule['desc']}</div>
  </div>
  <div class="rule-weight">+{rule['weight']:.2f}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    if false_alarm_active and float(live_hum) >= rh_safe:
        st.info(f"False-alarm filter active: PM spike is discounted because RH ≥ {rh_safe}%.")

    st.markdown("""
    <div class="system">
    <b>Fusion concept (with AI Hub)</b><br>
    Birdhouse does not replace AI — it <b>confirms</b> alerts using local evidence.<br>
    Strong local confirmation increases trust and can trigger <b>override escalation</b>.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("© 2026 NEXUS AI – Forest Smart Birdhouse")
