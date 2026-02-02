# =====================================
# NEXUS – AI HUB (CLEAN HEADER)
# =====================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import joblib
from fpdf import FPDF
import os

from utils import load_css, img_to_base64

# =====================================
# LOAD GLOBAL STYLE (ثابت)
# =====================================
load_css()

# =====================================
# HERO SECTION
# =====================================
hero_b64 = img_to_base64("assets/hero.png")

st.markdown(
    f"""
    <div class="hero-wrap">
        <img src="data:image/png;base64,{hero_b64}">
        <div class="hero-overlay"></div>
        <div class="hero-text">AI for Wildfire Prevention</div>
        <div class="hero-sub">Welcome to NEXUS platform about Climate + Sensors • Explainable AI</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================
# MAPBOX TOKEN (SAFE)
# =====================================
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN", "")
if MAPBOX_TOKEN:
    px.set_mapbox_access_token(MAPBOX_TOKEN)

# =====================================
# MODEL LOADING (CORE)
# =====================================
@st.cache_resource
def load_nexus_model():
    try:
        return joblib.load("fire_risk_model.pkl")
    except:
        return None

model = load_nexus_model()

# ============================================================
# 2) LANGUAGES (KEEP + EXTEND)
# ============================================================
LANGS = {
    "English": {
        "title": "🧠 NEXUS AI Hub",
        "subtitle": "Explainable wildfire decision intelligence.",
        "geo": "📍 Geospatial Analysis",
        "manual": "🎛️ Strategic Simulation",
        "execute": "Execute Neural Analysis",
        "sync": "Establish Live Satellite Link",
        "report": "Download AI Report (PDF)",
        "risk_label": "Fire Risk Index (FRI)",
        "risk_desc": "Normalized AI decision score reflecting ignition & spread potential.",
        "verdict": "System Verdict",
        "overview": "Decision Overview",
        "reasoning": "AI Reasoning",
        "analysis": "Factor Analysis",
        "whatif": "What-If Simulation",
        "baseline": "Baseline vs Yesterday",
        "dir": "ltr",
        "no_baseline": "No baseline yet (run once to set yesterday reference).",
        # NEW (Decision Summary tab)
        "decision_summary_tab": "AI Decision Summary",
        "gt_active": "Ground Truth Active",
        "using_birdhouse": "Using Birdhouse Node data",
        "sensor_unavailable": "Sensor data unavailable — fusion relies primarily on the climate model.",
        "fusion_overview": "Fusion Overview",
        "final_level": "Final Risk Level",
        "system_alerts": "System Alerts",
        "ai_explanation": "AI Explanation",
        "context_compare": "Contextual Comparison",
        # NEW (Trends / Sensitivity / Satellite / AQI)
        "trend_title": "Temporal Trend (Last 24h)",
        "trend_empty": "No temporal trend yet — run analysis to build the last-24h history.",
        "trend_up": "Trend: increasing risk",
        "trend_down": "Trend: decreasing risk",
        "trend_flat": "Trend: stable",
        "sensitivity_title": "Sensitivity Analysis",
        "sat_toggle": "Map Style",
        "sat_dark": "Dark (Analysis)",
        "sat_sat": "Satellite (Real View)",
        "aqi_title": "Air Quality Index (AQI)",
        "aqi_na": "AQI unavailable (requires Geo mode + valid coordinates).",
        "sys_health": "System Health",
        # NEW (Overview top section)
        "ov_title": "How NEXUS builds the decision",
        "ov_subtitle": "Data → AI Engine → Decision Output (transparent & explainable).",
        "ov_sources": "Data Sources",
        "ov_engine": "AI Engine",
        "ov_output": "Decision Output",
        "ov_live": "Live System Status",
        "ov_trust": "Why you can trust this",
        "ov_cta": "Run the AI to generate today’s decision",
        "ov_src_weather": "Satellite Weather (OpenWeather)",
        "ov_src_aqi": "Air Quality (OpenWeather AQI)",
        "ov_src_bird": "Ground Sensors (Birdhouse)",
        "ov_src_manual": "Manual Simulation (What-If)",
        "ov_eng_feat": "Feature engineering",
        "ov_eng_ml": "ML prediction (trained model)",
        "ov_eng_fusion": "Fusion logic (climate + ground truth)",
        "ov_eng_xai": "Explainable AI (drivers + contributions)",
        "ov_out_fri": "FRI score + risk category",
        "ov_out_alerts": "System alerts + recommendation",
        "ov_out_report": "PDF report generation",
        "ov_trust_xai": "Explainable: not a black box",
        "ov_trust_gt": "Ground truth aware (Birdhouse impact)",
        "ov_trust_scen": "Scenario aware (What-If + sensitivity)"
    },
    "Deutsch": {
        "title": "🧠 NEXUS KI-Zentrum",
        "subtitle": "Erklärbare KI für Waldbrand-Entscheidungen.",
        "geo": "📍 Geospatial-Analyse",
        "manual": "🎛️ Strategische Simulation",
        "execute": "KI-Analyse ausführen",
        "sync": "Satellitenverbindung herstellen",
        "report": "KI-Bericht herunterladen (PDF)",
        "risk_label": "Brandrisikoindex (FRI)",
        "risk_desc": "Normalisierter KI-Entscheidungswert für Zünd- und Ausbreitungspotenzial.",
        "verdict": "Systemurteil",
        "overview": "Entscheidungsübersicht",
        "reasoning": "KI-Begründung",
        "analysis": "Faktoranalyse",
        "whatif": "Was-wäre-wenn Simulation",
        "baseline": "Vergleich mit gestern",
        "dir": "ltr",
        "no_baseline": "Noch kein Basiswert (einmal ausführen, um Referenz zu setzen).",
        # NEW
        "decision_summary_tab": "AI Decision Summary",
        "gt_active": "Ground Truth Aktiv",
        "using_birdhouse": "Birdhouse-Knotendaten werden verwendet",
        "sensor_unavailable": "Sensordaten nicht verfügbar — Fusion basiert primär auf dem Klimamodell.",
        "fusion_overview": "Fusionsübersicht",
        "final_level": "Endgültiges Risikoniveau",
        "system_alerts": "Systemwarnungen",
        "ai_explanation": "KI-Erklärung",
        "context_compare": "Kontextvergleich",
        # NEW
        "trend_title": "Zeittrend (Letzte 24h)",
        "trend_empty": "Noch kein Zeittrend — führe die Analyse aus, um Verlauf aufzubauen.",
        "trend_up": "Trend: steigendes Risiko",
        "trend_down": "Trend: sinkendes Risiko",
        "trend_flat": "Trend: stabil",
        "sensitivity_title": "Sensitivitätsanalyse",
        "sat_toggle": "Kartenstil",
        "sat_dark": "Dunkel (Analyse)",
        "sat_sat": "Satellit (Realansicht)",
        "aqi_title": "Luftqualitätsindex (AQI)",
        "aqi_na": "AQI nicht verfügbar (Geo-Modus + gültige Koordinaten erforderlich).",
        "sys_health": "Systemstatus",
        # NEW (Overview top section)
        "ov_title": "Wie NEXUS die Entscheidung erzeugt",
        "ov_subtitle": "Daten → KI-Engine → Entscheidung (transparent & erklärbar).",
        "ov_sources": "Datenquellen",
        "ov_engine": "KI-Engine",
        "ov_output": "Entscheidungsoutput",
        "ov_live": "Live-Systemstatus",
        "ov_trust": "Warum das vertrauenswürdig ist",
        "ov_cta": "Starte die KI, um die Entscheidung zu erzeugen",
        "ov_src_weather": "Satellitenwetter (OpenWeather)",
        "ov_src_aqi": "Luftqualität (OpenWeather AQI)",
        "ov_src_bird": "Bodensensoren (Birdhouse)",
        "ov_src_manual": "Manuelle Simulation (What-If)",
        "ov_eng_feat": "Feature Engineering",
        "ov_eng_ml": "ML-Vorhersage (trainiertes Modell)",
        "ov_eng_fusion": "Fusionslogik (Klima + Ground Truth)",
        "ov_eng_xai": "Erklärbare KI (Treiber + Beiträge)",
        "ov_out_fri": "FRI-Score + Risikokategorie",
        "ov_out_alerts": "Warnungen + Empfehlung",
        "ov_out_report": "PDF-Bericht",
        "ov_trust_xai": "Erklärbar: keine Black Box",
        "ov_trust_gt": "Ground-Truth-bewusst (Birdhouse-Effekt)",
        "ov_trust_scen": "Szenario-bewusst (What-If + Sensitivität)"
    },
    "العربية": {
        "title": "🧠 مركز نكسوس للذكاء الاصطناعي",
        "subtitle": "ذكاء اصطناعي تفسيري لدعم القرار في مخاطر الحرائق.",
        "geo": "📍 التحليل الجغرافي",
        "manual": "🎛️ المحاكاة الاستراتيجية",
        "execute": "تشغيل التحليل",
        "sync": "تفعيل الاتصال بالقمر الصناعي",
        "report": "تحميل تقرير الذكاء الاصطناعي (PDF)",
        "risk_label": "مؤشر خطر الحريق (FRI)",
        "risk_desc": "قيمة قرار مُطبّعة تعبّر عن احتمال الاشتعال وسرعة الانتشار.",
        "verdict": "قرار النظام",
        "overview": "ملخص القرار",
        "reasoning": "منطق الذكاء الاصطناعي",
        "analysis": "تحليل العوامل",
        "whatif": "محاكاة ماذا لو؟",
        "baseline": "مقارنة مع عتبة أمس",
        "dir": "rtl",
        "no_baseline": "لا يوجد خط أساس بعد (شغّل مرة لتثبيت مرجع أمس).",
        # NEW
        "decision_summary_tab": "AI Decision Summary",
        "gt_active": "طبقة التحقق الأرضية مفعّلة",
        "using_birdhouse": "يتم استخدام بيانات Birdhouse",
        "sensor_unavailable": "بيانات الحساسات غير متاحة — الدمج يعتمد أساسًا على نموذج المناخ.",
        "fusion_overview": "ملخص الدمج",
        "final_level": "مستوى الخطر النهائي",
        "system_alerts": "تنبيهات النظام",
        "ai_explanation": "تفسير الذكاء الاصطناعي",
        "context_compare": "مقارنة سياقية",
        # NEW
        "trend_title": "تحليل الاتجاه (آخر 24 ساعة)",
        "trend_empty": "لا يوجد اتجاه بعد — شغّل التحليل لبناء سجل آخر 24 ساعة.",
        "trend_up": "الاتجاه: الخطر يتزايد",
        "trend_down": "الاتجاه: الخطر يتناقص",
        "trend_flat": "الاتجاه: ثابت تقريبًا",
        "sensitivity_title": "مصفوفة الحساسية",
        "sat_toggle": "نمط الخريطة",
        "sat_dark": "داكن (تحليل)",
        "sat_sat": "أقمار صناعية (واقع)",
        "aqi_title": "مؤشر جودة الهواء (AQI)",
        "aqi_na": "AQI غير متاح (يتطلب وضع Geo + إحداثيات صحيحة).",
        "sys_health": "حالة النظام",
        # NEW (Overview top section)
        "ov_title": "كيف يبني NEXUS القرار",
        "ov_subtitle": "البيانات → محرك الذكاء → مخرجات القرار (شفاف وتفسيري).",
        "ov_sources": "مصادر البيانات",
        "ov_engine": "محرك الذكاء الاصطناعي",
        "ov_output": "مخرجات القرار",
        "ov_live": "حالة النظام المباشرة",
        "ov_trust": "لماذا يمكن الوثوق بالنتيجة؟",
        "ov_cta": "شغّل التحليل للحصول على قرار اليوم",
        "ov_src_weather": "طقس مباشر (OpenWeather)",
        "ov_src_aqi": "جودة الهواء (AQI من OpenWeather)",
        "ov_src_bird": "حساسات أرضية (Birdhouse)",
        "ov_src_manual": "محاكاة يدوية (What-If)",
        "ov_eng_feat": "تجهيز الخصائص (Features)",
        "ov_eng_ml": "توقع ML (نموذج مدرّب)",
        "ov_eng_fusion": "منطق الدمج (مناخ + تحقق أرضي)",
        "ov_eng_xai": "تفسير القرار (Explainable AI)",
        "ov_out_fri": "درجة FRI + تصنيف الخطر",
        "ov_out_alerts": "تنبيهات + توصية",
        "ov_out_report": "تقرير PDF",
        "ov_trust_xai": "تفسيري: ليس صندوقًا أسود",
        "ov_trust_gt": "يعتمد على تحقق أرضي (أثر Birdhouse)",
        "ov_trust_scen": "يعرف السيناريوهات (What-If + حساسية)"
    }
}
# SIDEBAR STATE (من app.py)
# =====================================
if "lang" not in st.session_state:
    st.session_state.lang = "English"

T = LANGS[st.session_state.lang]

# ============================================================
# 3) PAGE CONFIG + SIDEBAR
# ============================================================
st.set_page_config(page_title="NEXUS AI | Full System", layout="wide", page_icon="🔥")

with st.sidebar:
    selected_lang = st.selectbox("🌐 Interface Language", ["English", "Deutsch", "العربية"])
    T = LANGS[selected_lang]
    st.divider()
    mode_selection = st.radio("System Mode", [T["geo"], T["manual"]])
    st.caption(f"Model Status: {'✅ Connected' if model else '❌ Offline'}")

# CSS (keep the dark premium feel) + NEW overview classes
st.markdown(f"""
<style>
/* 1. الخلفية الأساسية (بقت داكنة كما هي) */
.main {{
  direction: {T['dir']};
  text-align: {'right' if T['dir']=='rtl' else 'left'};
  background-color: #0b0f19;
  color: #000000 !important; /* الخط خارج الكروت أسود */
}}

/* 2. حل مشكلة النصوص في الصورة (Dark Analysis / Satellite) */
/* هذا الجزء يضمن أن نصوص الراديو والويدجت تصبح سوداء */
div[data-testid="stWidgetLabel"] p, 
div[role="radiogroup"] label, 
div[data-testid="stMarkdownContainer"] p {{
    color: #000000 !important;
}}

/* 3. الكروت (ألوانك الأصلية كما طلبت بدون تغيير) */
.status-card {{
  background: rgba(251, 146, 60, 0.15); 
  backdrop-filter: blur(12px);
  padding: 22px;
  border-radius: 16px;
  border: 1px solid #f97316;
  margin-top: 14px;
}}

.kpi-card {{
  background: rgba(234, 88, 12, 0.1); 
  border: 1px solid rgba(251, 146, 60, 0.4);
  border-radius: 16px;
  padding: 16px 18px;
}}

/* 4. إجبار اللون الأسود داخل الكروت لضمان الوضوح */
.kpi-card, .status-card, .ov-card, .ov-wrap {{
    color: #000000 !important;
}}

.kpi-card *, .status-card *, .ov-card *, .ov-wrap * {{
    color: #000000 !important;
}}

.small-muted {{
  color: #000000 !important; 
  font-size: 0.92rem;
  opacity: 0.8;
}}

/* 5. Overview (تنسيقك البرتقالي الأصلي) */
.ov-wrap {{
  background: rgba(124, 45, 18, 0.2);
  border: 1px solid #ea580c;
  border-radius: 18px;
  padding: 18px;
  margin: 10px 0 18px 0;
}}

.ov-title {{
  color: #000000 !important;
  font-size: 1.15rem;
  font-weight: 700;
}}

.ov-sub {{
  color: #000000 !important;
  font-size: 0.92rem;
  margin-top: 4px;
}}

.ov-card {{
  background: rgba(251, 146, 60, 0.05);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 14px;
  padding: 14px;
  height: 100%;
}}

.ov-pill {{
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid #f97316;
  background: rgba(249, 115, 22, 0.2);
  color: #000000 !important; /* حولتها لأسود لتناسب طلبك */
  font-size: 0.85rem;
  margin: 3px 6px 0 0;
}}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 4) HELPERS (Weather + Risk + Explain + PDF)
# ============================================================
OPENWEATHER_API_KEY = "2a2e9c8640d7faea05e8125ebeda0a52"

def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url, timeout=6).json()
        return {"t": float(res["main"]["temp"]), "h": float(res["main"]["humidity"]), "w": float(res["wind"]["speed"]) * 3.6}  # km/h
    except:
        return None

def get_aqi(lat, lon):
    """
    OpenWeather Air Pollution API:
    returns AQI 1..5 (1=Good, 5=Very Poor) + PM2.5 etc.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        res = requests.get(url, timeout=6).json()
        if not res or "list" not in res or not res["list"]:
            return None
        main = res["list"][0].get("main", {})
        comps = res["list"][0].get("components", {})
        aqi = int(main.get("aqi", 0))
        pm25 = float(comps.get("pm2_5", np.nan))
        pm10 = float(comps.get("pm10", np.nan))
        return {"aqi": aqi, "pm2_5": pm25, "pm10": pm10}
    except:
        return None

def aqi_label(aqi_int):
    # 1..5 per OpenWeather
    return {
        1: ("GOOD", "🟢"),
        2: ("FAIR", "🟡"),
        3: ("MODERATE", "🟠"),
        4: ("POOR", "🔴"),
        5: ("VERY POOR", "🟣")
    }.get(int(aqi_int), ("UNKNOWN", "⚪"))

def classify_risk(score_0_300):
    if score_0_300 < 80:
        return "LOW", "🟢"
    elif score_0_300 < 150:
        return "MODERATE", "🟡"
    elif score_0_300 < 220:
        return "HIGH", "🟠"
    else:
        return "EXTREME", "🔴"

def decision_recommendation(level):
    return {
        "LOW": "Normal conditions. No action required.",
        "MODERATE": "Monitoring recommended. Increase vigilance.",
        "HIGH": "Prepare response units. Increase surveillance & readiness.",
        "EXTREME": "Immediate emergency action advised. Activate response protocols."
    }.get(level, "Monitoring recommended.")

def compute_contributions_linear(model_obj, x_row):
    coef = getattr(model_obj, "coef_", None)
    if coef is None:
        return None, None
    coef = np.array(coef).reshape(-1)
    x = np.array(x_row).reshape(-1)
    if coef.shape[0] != x.shape[0]:
        return None, None
    contrib = coef * x
    return contrib, np.abs(coef)

def drivers_from_contrib(contrib, names):
    if contrib is None:
        return None, None
    idx_sorted = np.argsort(np.abs(contrib))[::-1]
    primary = (names[idx_sorted[0]], contrib[idx_sorted[0]])
    secondary = (names[idx_sorted[1]], contrib[idx_sorted[1]]) if len(names) > 1 else None
    return primary, secondary

def explain_text(features, primary=None, secondary=None):
    reasons = []
    if features["w"] > 40:
        reasons.append("strong wind increases spread potential")
    if features["h"] < 30:
        reasons.append("low humidity dries fuels")
    if features["t"] > 35:
        reasons.append("high temperature supports ignition")
    if not reasons:
        reasons.append("conditions are within a relatively safe range")
    driver_line = ""
    if primary:
        driver_line = f"Primary driver: {primary[0]}."
        if secondary:
            driver_line += f" Secondary: {secondary[0]}."
    return f"AI reasoning: {', '.join(reasons)}.\n{driver_line}".strip()

def pdf_safe(text):
    if text is None:
        return ""
    replacements = {
        "▬": "STABLE",
        "↑": "UP",
        "↓": "DOWN",
        "🟢": "LOW",
        "🟡": "MODERATE",
        "🟠": "HIGH",
        "🔴": "EXTREME"
    }
    for k, v in replacements.items():
        text = str(text).replace(k, v)
    return text.encode("latin-1", errors="ignore").decode("latin-1")

def generate_pdf(score, level, verdict, params, baseline_text, explanation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="NEXUS AI - Wildfire Intelligence Report", ln=True, align='C')
    pdf.ln(6)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=pdf_safe(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.cell(0, 8, txt=pdf_safe(f"Risk Score (FRI): {score:.2f} / 300"), ln=True)
    pdf.cell(0, 8, txt=pdf_safe(f"Risk Level: {level}"), ln=True)
    pdf.cell(0, 8, txt=pdf_safe(f"System Verdict: {verdict}"), ln=True)

    pdf.multi_cell(0, 8, txt=pdf_safe(f"Baseline vs Yesterday: {baseline_text}"))
    pdf.ln(2)
    pdf.multi_cell(0, 8, txt=pdf_safe(f"Explanation: {explanation}"))
    pdf.ln(2)
    pdf.multi_cell(0, 8, txt=pdf_safe(f"Inputs: {params}"))

    return pdf.output(dest='S').encode('latin-1')

# ============================================================
# NEW: TREND + FUSION + ALERTS + SENSITIVITY (helpers-in-file)
# ============================================================
def clamp01(x):
    try:
        return max(0.0, min(1.0, float(x)))
    except:
        return 0.0

def update_fri_history(score_ui):
    """
    Keeps a last-24h history inside session_state.
    If time jumps or app restarts, still works as rolling window.
    """
    now = datetime.now()
    rec = {"ts": now, "fri": float(score_ui)}
    hist = st.session_state.get("fri_history", [])
    hist.append(rec)

    # keep only last 24h
    cutoff = now - timedelta(hours=24)
    hist = [h for h in hist if h["ts"] >= cutoff]

    # hard cap to prevent growth (safety)
    if len(hist) > 240:
        hist = hist[-240:]

    st.session_state["fri_history"] = hist

def trend_status_from_history(hist):
    """
    Returns (label_key, slope) based on simple linear trend.
    """
    if not hist or len(hist) < 3:
        return None, 0.0
    dfh = pd.DataFrame(hist).copy()
    dfh = dfh.dropna()
    if dfh.empty:
        return None, 0.0

    # numeric time axis (minutes from start)
    t0 = dfh["ts"].min()
    x = (dfh["ts"] - t0).dt.total_seconds().values / 60.0
    y = dfh["fri"].values.astype(float)

    if len(np.unique(x)) < 2:
        return None, 0.0

    # slope (fri per minute)
    slope = np.polyfit(x, y, 1)[0]
    # map to status
    if slope > 0.015:   # ~ +0.9 per hour
        return "up", slope
    if slope < -0.015:  # ~ -0.9 per hour
        return "down", slope
    return "flat", slope

def compute_sensor_score_from_field(field_data: dict):
    """
    Converts Birdhouse field data to a 0..1 sensor_score.
    Uses only available keys (safe). If nothing usable exists, return None.
    Expected possible keys: t, h, pm25, smoke_pm25
    """
    if not isinstance(field_data, dict):
        return None

    pm = field_data.get("pm25", field_data.get("smoke_pm25", None))
    t = field_data.get("t", None)
    h = field_data.get("h", None)

    usable = False
    score = 0.0

    if pm is not None:
        try:
            pmv = float(pm)
            usable = True
            if pmv > 600:
                score += 0.60
            elif pmv > 200:
                score += 0.40
            elif pmv > 80:
                score += 0.25
        except:
            pass

    if h is not None:
        try:
            hv = float(h)
            usable = True
            if hv < 15:
                score += 0.35
            elif hv < 30:
                score += 0.25
            elif hv < 45:
                score += 0.10
        except:
            pass

    if t is not None:
        try:
            tv = float(t)
            usable = True
            if tv > 55:
                score += 0.25
            elif tv > 40:
                score += 0.18
            elif tv > 32:
                score += 0.10
        except:
            pass

    if not usable:
        return None

    return clamp01(score)

def compute_fusion_score(climate_0_1: float, sensor_0_1):
    c = clamp01(climate_0_1)
    if sensor_0_1 is None:
        return clamp01(0.90 * c)
    s = clamp01(sensor_0_1)
    return clamp01(0.60 * c + 0.40 * s)

def fusion_level(fusion_0_1: float):
    f = clamp01(fusion_0_1)
    if f < 0.30:
        return "LOW", "🟢"
    elif f < 0.60:
        return "MODERATE", "🟡"
    elif f < 0.80:
        return "HIGH", "🟠"
    else:
        return "EXTREME", "🔴"

def generate_system_alerts(fusion_0_1, sensor_0_1, delta_ui, baseline_available: bool, aqi_pack=None):
    alerts = []
    f = clamp01(fusion_0_1)

    if f >= 0.80:
        alerts.append("🔴 Critical escalation: fusion indicates EXTREME conditions.")
    elif f >= 0.60:
        alerts.append("🟠 Elevated conditions: fusion indicates HIGH risk.")
    elif f >= 0.30:
        alerts.append("🟡 Moderate conditions: maintain monitoring.")
    else:
        alerts.append("🟢 Low conditions: routine monitoring.")

    if sensor_0_1 is None:
        alerts.append("⚠️ Sensor feed unavailable: decision weighted toward climate model.")
    else:
        if sensor_0_1 >= 0.75:
            alerts.append("🔥 Sensor escalation detected: ground truth signals are critical.")
        elif sensor_0_1 >= 0.55:
            alerts.append("⚠️ Sensor escalation detected: ground truth signals are moderate.")

    if baseline_available:
        try:
            d = float(delta_ui)
            if d > 10:
                alerts.append("⬆️ Significant increase vs yesterday baseline.")
            elif d < -10:
                alerts.append("⬇️ Significant decrease vs yesterday baseline.")
        except:
            pass

    # AQI reinforcement
    if aqi_pack and isinstance(aqi_pack, dict):
        aqi_val = aqi_pack.get("aqi", None)
        try:
            aqi_val = int(aqi_val)
            if aqi_val >= 4 and f >= 0.60:
                alerts.append("🌫️ Elevated AQI reinforces potential nearby smoke/combustion evidence.")
        except:
            pass

    return alerts

def decision_explanation_text(final_features, fusion_f, fusion_lvl, sensor_score, aqi_pack=None):
    lines = []
    lines.append(f"Fusion decision: {fusion_lvl} (score={fusion_f:.2f}).")

    reasons = []
    try:
        if final_features["w"] > 40:
            reasons.append("wind supports spread")
        if final_features["h"] < 30:
            reasons.append("low humidity dries fuels")
        if final_features["t"] > 35:
            reasons.append("heat supports ignition")
    except:
        pass

    if reasons:
        lines.append("Climate drivers: " + ", ".join(reasons) + ".")
    else:
        lines.append("Climate drivers: within safer range.")

    if sensor_score is None:
        lines.append("Ground truth: unavailable (climate-only fusion weighting).")
    else:
        if sensor_score >= 0.75:
            lines.append("Ground truth: critical escalation detected by sensors.")
        elif sensor_score >= 0.55:
            lines.append("Ground truth: moderate escalation detected by sensors.")
        else:
            lines.append("Ground truth: no significant escalation detected.")

    if aqi_pack and isinstance(aqi_pack, dict):
        aqi_val = aqi_pack.get("aqi", None)
        if aqi_val:
            lab, ic = aqi_label(aqi_val)
            lines.append(f"Secondary evidence: AQI={aqi_val} ({ic} {lab}).")

    return " ".join(lines)

def predict_score_ui(model_obj, features_dict):
    X = np.array([[features_dict["t"], features_dict["h"], features_dict["w"]]], dtype=float)
    raw = float(model_obj.predict(X)[0])
    score = max(0.0, raw)
    return min(300.0, score)

def compute_sensitivity_table(model_obj, base_features, base_score_ui):
    """
    Builds a small table: single-factor perturbations and resulting % change.
    """
    scenarios = [
        ("+5°C Temperature", {"t": base_features["t"] + 5, "h": base_features["h"], "w": base_features["w"]}),
        ("-10% Humidity", {"t": base_features["t"], "h": base_features["h"] - 10, "w": base_features["w"]}),
        ("+10 km/h Wind", {"t": base_features["t"], "h": base_features["h"], "w": base_features["w"] + 10}),
    ]

    rows = []
    for name, feat in scenarios:
        feat2 = {
            "t": float(np.clip(feat["t"], -30, 60)),
            "h": float(np.clip(feat["h"], 0, 100)),
            "w": float(np.clip(feat["w"], 0, 200))
        }
        s2 = predict_score_ui(model_obj, feat2)
        delta = s2 - float(base_score_ui)
        pct = (delta / float(base_score_ui) * 100.0) if float(base_score_ui) != 0 else 0.0
        rows.append({"Scenario": name, "ΔFRI": round(delta, 1), "Δ%": round(pct, 1)})

    df = pd.DataFrame(rows)
    df["AbsImpact"] = df["Δ%"].abs()
    df = df.sort_values("AbsImpact", ascending=False).drop(columns=["AbsImpact"])
    return df

# ============================================================
# 5) HEADER
# ============================================================
st.title(T["title"])
st.markdown(f"<p class='small-muted'>{T['subtitle']}</p>", unsafe_allow_html=True)

# ============================================================
# NEW: TOP OVERVIEW (ABOVE INPUTS) — Data → AI → Decision + Live Status
# ============================================================
# Live status snapshot (real, based on session_state + loaded model)
_model_ok = bool(model)
_weather_ok = True if (mode_selection == T["manual"] or ("data_link" in st.session_state)) else False
_aqi_ok = True if isinstance(st.session_state.get("aqi_pack", None), dict) and st.session_state.get("aqi_pack", {}).get("aqi", None) else False
_bird_ok = True if isinstance(st.session_state.get("field_data", None), dict) else False
_fusion_state = "Active ✅" if (_model_ok and (_weather_ok or mode_selection == T["manual"])) else "Inactive ⚠️"

src_online = sum([_model_ok, _weather_ok, _aqi_ok, _bird_ok])
src_total = 4

st.markdown(f"""
<div class="ov-wrap">
  <div class="ov-title">🧭 {T.get("ov_title","How NEXUS builds the decision")}</div>
  <div class="ov-sub">{T.get("ov_subtitle","Data → AI Engine → Decision Output (transparent & explainable).")}</div>
  <div style="margin-top:10px">
    <span class="ov-pill">🤖 Model: {'✅' if _model_ok else '❌'}</span>
    <span class="ov-pill">🛰️ Weather: {'✅' if _weather_ok else '⚠️'}</span>
    <span class="ov-pill">🌫️ AQI: {'✅' if _aqi_ok else '⚠️'}</span>
    <span class="ov-pill">🌲 Birdhouse: {'✅' if _bird_ok else '⚠️'}</span>
    <span class="ov-pill">🧩 Fusion: {_fusion_state}</span>
    <span class="ov-pill">📡 Sources Online: {src_online}/{src_total}</span>
  </div>
</div>
""", unsafe_allow_html=True)

ov1, ov2, ov3 = st.columns(3)

with ov1:
    st.markdown(f"""
    <div class="ov-card">
      <b>1️⃣ {T.get("ov_sources","Data Sources")}</b><br>
      • {T.get("ov_src_weather","Satellite Weather (OpenWeather)")}<br>
      • {T.get("ov_src_aqi","Air Quality (OpenWeather AQI)")}<br>
      • {T.get("ov_src_bird","Ground Sensors (Birdhouse)")}<br>
      • {T.get("ov_src_manual","Manual Simulation (What-If)")}<br>
      <div class="ov-sub" style="margin-top:8px">
        Inputs arrive either from live APIs (Geo mode), from local sensors (Birdhouse), or from manual scenario controls.
      </div>
    </div>
    """, unsafe_allow_html=True)

with ov2:
    st.markdown(f"""
    <div class="ov-card">
      <b>2️⃣ {T.get("ov_engine","AI Engine")}</b><br>
      • {T.get("ov_eng_feat","Feature engineering")}<br>
      • {T.get("ov_eng_ml","ML prediction (trained model)")}<br>
      • {T.get("ov_eng_fusion","Fusion logic (climate + ground truth)")}<br>
      • {T.get("ov_eng_xai","Explainable AI (drivers + contributions)")}<br>
      <div class="ov-sub" style="margin-top:8px">
        The model predicts a climate risk score, then fusion optionally adjusts it using ground-truth confirmation.
      </div>
    </div>
    """, unsafe_allow_html=True)

with ov3:
    st.markdown(f"""
    <div class="ov-card">
      <b>3️⃣ {T.get("ov_output","Decision Output")}</b><br>
      • {T.get("ov_out_fri","FRI score + risk category")}<br>
      • {T.get("ov_out_alerts","System alerts + recommendation")}<br>
      • {T.get("ov_out_report","PDF report generation")}<br>
      <div class="ov-sub" style="margin-top:8px">
        Output is not just a number: it includes drivers, trend context, alerts, and recommended actions.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# Trend area (always visible if history exists)
# ============================================================
with st.container():
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader(f"⏱️ {T['trend_title']}")
    hist = st.session_state.get("fri_history", [])
    if not hist or len(hist) < 2:
        st.info(T["trend_empty"])
    else:
        dfh = pd.DataFrame(hist).copy()
        dfh["ts"] = pd.to_datetime(dfh["ts"])
        dfh = dfh.sort_values("ts")
        dfh = dfh.set_index("ts")[["fri"]]
        st.line_chart(dfh, height=160)

        status, slope = trend_status_from_history(hist)
        if status == "up":
            st.warning(T["trend_up"])
        elif status == "down":
            st.success(T["trend_down"])
        else:
            st.info(T["trend_flat"])
    st.markdown("</div>", unsafe_allow_html=True)

final_features = None
lat, lon = None, None
aqi_pack = None

# ============================================================
# 6) INPUTS (Geo / Manual) + MAP STYLE TOGGLE + AQI
# ============================================================
if mode_selection == T["geo"]:
    c_geo1, c_geo2 = st.columns([1, 2])

    with c_geo1:
        st.subheader("🛰️ Precision Targeting")
        lat = st.number_input("Latitude", value=52.5200, format="%.4f")
        lon = st.number_input("Longitude", value=13.4050, format="%.4f")

        # Map style toggle (NEW)
        map_style_choice = st.radio(
            T["sat_toggle"],
            [T["sat_dark"], T["sat_sat"]],
            horizontal=True
        )
        map_style = (
    "carto-darkmatter"
    if map_style_choice == T["sat_dark"]
    else ("satellite-streets" if MAPBOX_TOKEN else "open-street-map")
)


        if st.button(T["sync"], use_container_width=True):
            w = get_weather(lat, lon)
            if w:
                st.session_state["data_link"] = w
            # AQI fetch along with sync (NEW)
            aqi = get_aqi(lat, lon)
            if aqi:
                st.session_state["aqi_pack"] = aqi

        if "data_link" in st.session_state:
            dl = st.session_state["data_link"]
            st.info(f"🌡️ {dl['t']:.1f}°C | 💨 {dl['w']:.1f} km/h | 💧 {dl['h']:.0f}%")
            final_features = {"t": dl["t"], "h": dl["h"], "w": dl["w"]}

        # AQI telemetry display (NEW)
        aqi_pack = st.session_state.get("aqi_pack", None)
        st.markdown(" ")
        st.subheader(f"🌫️ {T['aqi_title']}")
        if aqi_pack and isinstance(aqi_pack, dict) and aqi_pack.get("aqi", None):
            lab, ic = aqi_label(aqi_pack["aqi"])
            st.write(f"**AQI:** {aqi_pack['aqi']}  {ic}  **{lab}**")
            if not np.isnan(aqi_pack.get("pm2_5", np.nan)):
                st.write(f"PM2.5: {aqi_pack['pm2_5']:.1f} µg/m³")
            if not np.isnan(aqi_pack.get("pm10", np.nan)):
                st.write(f"PM10: {aqi_pack['pm10']:.1f} µg/m³")
        else:
            st.caption(T["aqi_na"])

    with c_geo2:
        st.subheader("🗺️ Location Map")
        df_map = pd.DataFrame([{"lat": lat if lat is not None else 52.5200, "lon": lon if lon is not None else 13.4050}])

        fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", zoom=9, height=360)
        fig_map.update_layout(
            mapbox_style=map_style,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=360
        )
        fig_map.update_traces(marker=dict(size=18, color="#ff4b4b"))
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

else:
    st.subheader(T["manual"])
    m_c1, m_c2, m_c3 = st.columns(3)
    sm_t = m_c1.slider("Temperature (°C)", 0, 50, 30)
    sm_h = m_c2.slider("Humidity (%)", 0, 100, 35)
    sm_w = m_c3.slider("Wind Speed (km/h)", 0, 120, 25)
    final_features = {"t": float(sm_t), "h": float(sm_h), "w": float(sm_w)}

    # keep AQI pack as None in manual mode
    aqi_pack = None

# ============================================================
# 7) EXECUTE BUTTON (kept) + RESULTS with 5 TABS
# ============================================================
if st.button(T["execute"], type="primary", use_container_width=True):
    if model and final_features:

        # ----------------------------------------------------
        # 1) MODEL INFERENCE
        # ----------------------------------------------------
        prev_score = st.session_state.get("prev_score", None)

        X = np.array([[final_features["t"], final_features["h"], final_features["w"]]], dtype=float)
        raw_pred = float(model.predict(X)[0])

        score = max(0.0, raw_pred)
        score_ui = min(300.0, score)

        # NEW: update 24h trend history
        update_fri_history(score_ui)

        level, icon = classify_risk(score_ui)

        # ----------------------------------------------------
        # 2) BASELINE (Yesterday comparison)
        # ----------------------------------------------------
        if prev_score is None:
            baseline_text = T["no_baseline"]
            delta_text = "—"
            delta_pct_text = "—"
            delta_for_alerts = 0.0
            baseline_available = False
        else:
            delta = score_ui - float(prev_score)
            delta_pct = (delta / float(prev_score) * 100.0) if float(prev_score) != 0 else 0.0
            arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "▬")
            delta_text = f"{arrow} {delta:+.1f}"
            delta_pct_text = f"{delta_pct:+.1f}%"
            baseline_text = f"{delta_text} ({delta_pct_text}) vs yesterday baseline"
            delta_for_alerts = float(delta)
            baseline_available = True

        st.session_state["prev_score"] = score_ui
        verdict_str = level

        # ----------------------------------------------------
        # 3) EXPLAINABILITY
        # ----------------------------------------------------
        feat_names = ["Temp", "Hum", "Wind"]
        contrib, coef_abs = compute_contributions_linear(model, X[0])
        primary, secondary = drivers_from_contrib(contrib, feat_names)

        explanation = explain_text(final_features, primary, secondary)
        recommendation = decision_recommendation(level)

        # Confidence (simple, product-friendly)
        confidence = min(0.95, max(0.55, score_ui / 300.0))

        # ----------------------------------------------------
        # 4) SYSTEM HEALTH STRIP
        # ----------------------------------------------------
        with st.container():
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.subheader(f"🧾 {T['sys_health']}")
            h1, h2, h3 = st.columns(3)

            with h1:
                st.metric("Model", "Connected ✅" if model else "Offline ❌")

            with h2:
                weather_ok = True if (mode_selection == T["manual"] or "data_link" in st.session_state) else False
                st.metric("Weather Link", "OK ✅" if weather_ok else "Not synced ⚠️")

            with h3:
                birdhouse = st.session_state.get("field_data", None)
                st.metric("Birdhouse", "Active ✅" if isinstance(birdhouse, dict) else "Unavailable ⚠️")

            st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # 5) TOP KPI STRIP
        # ----------------------------------------------------
        k1, k2, k3, k4 = st.columns([1.35, 1.1, 1.1, 1.45])

        with k1:
            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.markdown(f"### {T['risk_label']}")
            st.markdown(f"<div class='small-muted'>{T['risk_desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"## {score_ui:.1f} / 300")
            st.markdown("</div>", unsafe_allow_html=True)

        with k2:
            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.markdown("### Risk Category")
            st.markdown(f"## {icon} {level}")
            st.markdown("</div>", unsafe_allow_html=True)

        with k3:
            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.markdown(f"### {T['baseline']}")
            st.markdown(f"## {delta_text}")
            st.markdown(f"<div class='small-muted'>{baseline_text}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with k4:
            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.markdown("### AI Confidence")
            st.progress(confidence)
            st.markdown(f"<div class='small-muted'>Confidence: {confidence*100:.1f}%</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ====================================================
        # 🔁 NEW: GROUND TRUTH IMPACT (Before / After)
        # ====================================================
        st.markdown("## 🔁 Ground Truth Impact – Birdhouse Effect")
        st.caption("How local sensor confirmation changes the AI decision")

        climate_only_score = score_ui / 300.0
        before_confidence = 0.55

        birdhouse_data = st.session_state.get("field_data")

        if birdhouse_data:
            smoke_factor = min(birdhouse_data.get("pm25", 240) / 600.0, 1.0)
            dryness_factor = 1.0 if birdhouse_data.get("h", 50) < 30 else 0.4
            sensor_score = 0.6 * smoke_factor + 0.4 * dryness_factor

            after_fusion = 0.6 * climate_only_score + 0.4 * sensor_score
            after_confidence = min(0.9, before_confidence + 0.25)
        else:
            after_fusion = None
            after_confidence = None

        cA, cB, cC = st.columns([1.2, 0.6, 1.2])

        with cA:
            st.markdown("### ⬅️ Before (Climate only)")
            st.metric("Fusion Score", round(climate_only_score, 2))
            st.progress(before_confidence)
            st.caption("No local confirmation")

        with cB:
            st.markdown("### Δ Impact")
            if after_fusion is not None:
                st.metric("Δ Risk", f"{after_fusion - climate_only_score:+.2f}")
                st.metric("Δ Confidence", f"{(after_confidence - before_confidence)*100:.0f}%")
            else:
                st.info("Waiting for Birdhouse data")

        with cC:
            st.markdown("### ➡️ After (Climate + Birdhouse)")
            if after_fusion is not None:
                st.metric("Fusion Score", round(after_fusion, 2))
                st.progress(after_confidence)
                st.caption("Ground truth detected")
            else:
                st.warning("Birdhouse inactive")

        # ----------------------------------------------------
        # 6) TABS
        # ----------------------------------------------------
        tab_overview, tab_decision, tab_reasoning, tab_analysis, tab_whatif = st.tabs(
            [
                f"✅ {T['overview']}",
                f"🧩 {T['decision_summary_tab']}",
                f"🧠 {T['reasoning']}",
                f"📊 {T['analysis']}",
                f"🔁 {T['whatif']}"
            ]
        )

        # -------------------------
        # TAB 1: Decision Overview
        # -------------------------
        with tab_overview:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            colA, colB = st.columns([1.35, 1.0])

            with colA:
                st.subheader("📍 Decision Summary")
                st.write(f"**{T['verdict']}:** {icon} **{level}**")
                st.write(f"**AI Summary:** Current conditions indicate **{level}** risk; baseline trend: **{delta_text}**.")
                st.info(f"**AI Recommendation:** {recommendation}")

                pdf_data = generate_pdf(score_ui, level, verdict_str, final_features, baseline_text, explanation)
                st.download_button(
                    label=T["report"],
                    data=pdf_data,
                    file_name="NEXUS_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with colB:
                st.subheader("🔥 FRI Gauge")
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score_ui,
                    number={"suffix": " / 300"},
                    gauge={
                        "axis": {"range": [0, 300]},
                        "bar": {"color": "#ef4444" if score_ui >= 220 else ("#f59e0b" if score_ui >= 150 else ("#eab308" if score_ui >= 80 else "#22c55e"))},
                        "steps": [
                            {"range": [0, 80], "color": "rgba(34,197,94,0.18)"},
                            {"range": [80, 150], "color": "rgba(234,179,8,0.18)"},
                            {"range": [150, 220], "color": "rgba(245,158,11,0.18)"},
                            {"range": [220, 300], "color": "rgba(239,68,68,0.18)"},
                        ]
                    }
                ))
                fig_gauge.update_layout(
                    height=290,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={"color": "white"}
                )
                st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # TAB 2: AI Decision Summary (VERTICAL)
        # -------------------------
        with tab_decision:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)

            field_data = st.session_state.get("field_data", None)
            if isinstance(field_data, dict):
                src = field_data.get("source", "Birdhouse Node")
                st.markdown(
                    f"""
                    <div class="gt-banner">
                      <span class="gt-badge">✅ {T['gt_active']}</span>
                      <span class="small-muted">{T['using_birdhouse']} — <b>{src}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # 1) Fusion Overview
            st.subheader(f"🧩 {T['fusion_overview']}")
            climate_0_1 = float(score_ui) / 300.0
            sensor_score = compute_sensor_score_from_field(field_data) if isinstance(field_data, dict) else None
            fusion = compute_fusion_score(climate_0_1, sensor_score)
            f_level, f_icon = fusion_level(fusion)

            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.write(f"**Climate Score:** {climate_0_1:.2f} (from FRI)")
            if sensor_score is None:
                st.write("**Sensor Score:** Unavailable")
                st.markdown(f"<div class='warn-banner'>{T['sensor_unavailable']}</div>", unsafe_allow_html=True)
            else:
                st.write(f"**Sensor Score:** {sensor_score:.2f} (Birdhouse)")
            st.write(f"**Fusion Score:** {fusion:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.divider()

            # 2) Final Risk Level
            st.subheader(f"🔥 {T['final_level']}")
            st.markdown(f"### {f_icon} **{f_level}**")

            st.divider()

            # 3) System Alerts
            st.subheader(f"🚨 {T['system_alerts']}")
            alerts = generate_system_alerts(fusion, sensor_score, delta_for_alerts, baseline_available, aqi_pack=aqi_pack)
            for a in alerts:
                st.markdown(f"- {a}")

            st.divider()

            # 4) AI Explanation
            st.subheader(f"🧠 {T['ai_explanation']}")
            expl = decision_explanation_text(final_features, fusion, f_level, sensor_score, aqi_pack=aqi_pack)
            st.success(expl)

            st.divider()

            # 5) Contextual Comparison
            st.subheader(f"📈 {T['context_compare']}")
            st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
            st.write(f"**Today FRI:** {score_ui:.1f} / 300")
            st.write(f"**Baseline vs Yesterday:** {baseline_text}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # TAB 3: AI Reasoning
        # -------------------------
        with tab_reasoning:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.subheader("🧠 How the AI reached this decision")
            st.caption("Transparent pipeline + decision drivers (not a black box).")

            st.markdown("""
**Decision Path**
- **Climate Data Ingestion** → Inputs acquired (manual sliders or live weather link)
- **Feature Engineering** → Features formatted and normalized for inference
- **ML Prediction** → Model computes risk score
- **Risk Logic Evaluation** → Score mapped to risk category thresholds
- **Decision Output** → Recommendation produced for readiness & action
""")

            # AQI evidence (NEW)
            if aqi_pack and isinstance(aqi_pack, dict) and aqi_pack.get("aqi", None):
                lab, ic = aqi_label(aqi_pack["aqi"])
                st.info(f"Secondary Evidence: AQI={aqi_pack['aqi']} ({ic} {lab}) — supports environmental validation.")

            st.subheader("🎯 Primary & Secondary Drivers")
            if primary:
                st.write(f"**Primary Driver:** {primary[0]}  (relative influence: {primary[1]:+.3f})")
            if secondary:
                st.write(f"**Secondary Driver:** {secondary[0]}  (relative influence: {secondary[1]:+.3f})")

            st.subheader("📝 Explanation")
            st.success(explanation)

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # TAB 4: Factor Analysis
        # -------------------------
        with tab_analysis:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.subheader("📊 Factor Contribution Analysis")
            st.caption("Shows which variables push the risk up or down.")

            if contrib is not None:
                df_c = pd.DataFrame({"Factor": feat_names, "Contribution": contrib}).sort_values("Contribution")
                fig_c = px.bar(df_c, x="Contribution", y="Factor", orientation="h", height=260)
                fig_c.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "white"},
                    showlegend=False
                )
                st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})
                st.markdown("**Interpretation:** Positive contribution increases risk; negative reduces risk.")
            else:
                st.info("Model contribution analysis unavailable for this model type.")

            st.markdown("</div>", unsafe_allow_html=True)

        # -------------------------
        # TAB 5: What-If Simulation + Sensitivity Matrix (NEW)
        # -------------------------
        with tab_whatif:
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            st.subheader("🔁 Scenario Simulation – What If Conditions Change?")
            st.caption("Interactively explore how changes affect the risk decision.")

            w1, w2, w3 = st.columns(3)
            with w1:
                dT = st.slider("Δ Temperature (°C)", -10, 10, 0)
            with w2:
                dH = st.slider("Δ Humidity (%)", -30, 30, 0)
            with w3:
                dW = st.slider("Δ Wind (km/h)", -30, 30, 0)

            sim_features = {
                "t": float(np.clip(final_features["t"] + dT, -30, 60)),
                "h": float(np.clip(final_features["h"] + dH, 0, 100)),
                "w": float(np.clip(final_features["w"] + dW, 0, 200))
            }

            X_sim = np.array([[sim_features["t"], sim_features["h"], sim_features["w"]]], dtype=float)
            sim_raw = float(model.predict(X_sim)[0])
            sim_score = max(0.0, sim_raw)
            sim_score_ui = min(300.0, sim_score)

            sim_level, sim_icon = classify_risk(sim_score_ui)

            sA, sB, sC = st.columns([1.2, 1.2, 1.6])
            with sA:
                st.markdown("### Current")
                st.write(f"**FRI:** {score_ui:.1f} / 300")
                st.write(f"**Category:** {icon} {level}")
                st.write(f"**Inputs:** T={final_features['t']:.1f}°C, H={final_features['h']:.0f}%, W={final_features['w']:.1f} km/h")

            with sB:
                st.markdown("### Simulated")
                st.write(f"**FRI:** {sim_score_ui:.1f} / 300")
                st.write(f"**Category:** {sim_icon} {sim_level}")
                st.write(f"**Inputs:** T={sim_features['t']:.1f}°C, H={sim_features['h']:.0f}%, W={sim_features['w']:.1f} km/h")

            with sC:
                st.markdown("### Impact")
                diff = sim_score_ui - score_ui
                arrow = "↑" if diff > 0 else ("↓" if diff < 0 else "▬")
                st.metric("Δ Risk (Sim - Current)", f"{diff:+.1f}", delta=f"{arrow}")
                st.info(f"**Simulation Note:** {decision_recommendation(sim_level)}")

            # Sensitivity Matrix (NEW)
            st.divider()
            st.subheader(f"📌 {T['sensitivity_title']}")
            sens_df = compute_sensitivity_table(model, final_features, score_ui)

            # highlight most sensitive row
            if not sens_df.empty:
                top = sens_df.iloc[0]
                st.markdown(
                    f"<div class='warn-banner'>Most sensitive factor right now: <b>{top['Scenario']}</b> (Δ% = {top['Δ%']}%)</div>",
                    unsafe_allow_html=True
                )

            st.dataframe(sens_df, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("Data missing: Please establish satellite link or set manual parameters (and ensure model is connected).")

st.divider()
st.caption("© 2026 NEXUS AI Systems | Integrated Forest Safety Platform")