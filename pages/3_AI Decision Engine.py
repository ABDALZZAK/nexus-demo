import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import math
from utils import img_to_base64
import streamlit as st
from utils import load_css

load_css()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NEXUS AI | AI Decision Engine",
    page_icon="🧩",
    layout="wide"
)

# ============================================================
# MULTI-LANGUAGE (extended with academic concept text)
# ============================================================
LANGS = {
    "English": {
        "title": "🧩 AI Decision Engine",
        "subtitle": "Climate-driven prediction • Sensor confirmation • Decision support",
        "controls": "⚙️ Controls",
        "date": "📅 Date",
        "risk_level": "🔥 Risk level",
        "map_settings": "🗺️ Map Settings",
        "view_mode": "View mode",
        "risk_thr": "Risk threshold",
        "radius": "Cluster radius (km)",
        "min_pts": "Min points",
        "tabs": ["🗺️ Map", "🧠 Decision Summary",  "🏛️ States", "🧪 Scenario", "⚖️ Compare"],
        "scenario_inactive": "🟡 Scenario inactive — run a scenario to enable comparison",
        "scenario_active": "🟢 Scenario active — comparison enabled",
        "no_sensors": "No sensor data available.",
        "sensor_map_title": "🗺️ Active Birdhouse Nodes",
        "sensor_map_caption": "Only nodes with meaningful local signals (sensor_score > threshold) are highlighted.",
        "forecast_title": "🔮 Forecast Horizon",
        "forecast_caption": "A simple, explainable forecast indicator based on recent trend + assumptions.",
        "proximity_title": "🚒 Proximity",
        "proximity_caption": "Operational context: distance & estimated response time to nearest fire station.",
        "alerts_title": "🔔 Alerts",
        "alerts_caption": "Actionable alerts derived from climate trend + sensors + fusion.",
        "subscribe": "Subscribe to Alerts",
        "subscribe_hint": "Demo: stores your preference in session_state (no emails sent).",
        "on": "ON",
        "off": "OFF",
        "fusion": "Fusion Score",
        "final_level": "🔥 FINAL LEVEL",
        "kpi_cells": "Grid cells",
        "kpi_hi": "High / Extreme",
        "kpi_avg": "Avg risk score",
        "kpi_date": "Date",
        "legend": "🎨 Risk Legend",
        "delta_legend": "🎨 Δ Risk Legend",
        "compare_hint": "No scenario executed yet. Go to Scenario tab and click Run Scenario.",
        "run_scenario": "Run Scenario",
        "run": "Run",
        "scenario_title": "🧪 What-If Analysis (Scenario Simulator)",
        "scenario_text": "Simulate what-if climate scenarios and assess their impact on wildfire risk.",
        "map_title": "🗺️ Spatial Wildfire Risk",
        "state_title": "🏛️ Risk by State",
        "decision_title": "🧠 Final Decision & Interpretation",
        "auto_explain": "🧠 Auto Explanation",
        "sensor_timeline": "⏱️ Sensor Risk Timeline",
        "trend_title": "⏱️ Trend (last days)",
        "trend_empty": "Trend history will appear after multiple days are available.",
        "dir": "ltr",

        # NEW: Academic / concept text (Decision Engine storyline)
        "concept_block_title": "Concept Overview",
        "concept_block_text": (
            "The AI Decision Engine is the operational layer that converts heterogeneous evidence into an actionable wildfire "
            "risk decision. It aggregates (i) **climate-driven spatial risk** from gridded datasets, (ii) **ground-truth "
            "confirmation** from Birdhouse sensor nodes, and (iii) **decision support context** such as trend, hotspots, and "
            "response proximity. The result is a transparent decision pipeline: **observe → fuse → interpret → act**."
        ),
        "map_concept_title": "Why the map exists",
        "map_concept_text": (
            "The spatial map provides situational awareness: it shows where risk is concentrated, how it is distributed across "
            "the territory, and which locations exceed operational thresholds. This enables prioritization of surveillance and "
            "resource allocation."
        ),
        "summary_concept_title": "How the final decision is formed",
        "summary_concept_text": (
            "The final level is derived from a **fusion score** that combines the climate signal (model-based risk) with the "
            "strongest available sensor confirmation (local evidence). This design reduces false alarms and improves trust: "
            "when climate risk is elevated but sensors are quiet, escalation is conservative; when both agree, the system "
            "escalates decisively."
        ),
        "why_sensor_map_title": "Why the Birdhouse map and table are here",
        "why_sensor_map_text": (
            "The Birdhouse map and the accompanying table provide traceable ground-truth evidence. They identify which nodes "
            "contribute meaningful signals, where they are located, and what their measured indicators are (e.g., PM2.5, RH, "
            "temperature). This supports auditability and operational decisions such as dispatching field checks."
        ),
        "forecast_explain_title": "What the forecast indicates",
        "forecast_explain_text": (
            "The forecast is an explainable indicator derived from recent-day risk evolution. It does not replace the core "
            "model; instead, it communicates whether conditions are *increasing*, *decreasing*, or *stable* within the selected "
            "horizon, helping planners anticipate near-term escalation."
        ),
        "proximity_explain_title": "Why proximity is included",
        "proximity_explain_text": (
            "Proximity adds an operational constraint: the same risk level can have different implications depending on "
            "expected response time. By estimating distance and response latency to nearby fire stations, the engine supports "
            "readiness and resource staging."
        ),
        "alerts_explain_title": "Why alerts are generated",
        "alerts_explain_text": (
            "Alerts translate analytics into actions. They summarize the most important escalations derived from state trends, "
            "sensor anomalies, and fusion thresholds, enabling a short, decision-ready list rather than raw telemetry."
        ),
    },
    "Deutsch": {
        "title": "🧩 KI-Entscheidungsmodul",
        "subtitle": "Klima-Prognose • Sensor-Bestätigung • Entscheidungsunterstützung",
        "controls": "⚙️ Steuerung",
        "date": "📅 Datum",
        "risk_level": "🔥 Risikostufe",
        "map_settings": "🗺️ Karten-Einstellungen",
        "view_mode": "Ansicht",
        "risk_thr": "Risikoschwelle",
        "radius": "Cluster-Radius (km)",
        "min_pts": "Min Punkte",
        "tabs": ["🗺️ Karte", "🧠 Entscheidungsübersicht", "🏛️ Bundesländer", "🧪 Szenario", "⚖️ Vergleich"],
        "scenario_inactive": "🟡 Szenario inaktiv — führe ein Szenario aus, um den Vergleich zu aktivieren",
        "scenario_active": "🟢 Szenario aktiv — Vergleich aktiviert",
        "no_sensors": "Keine Sensordaten verfügbar.",
        "sensor_map_title": "🗺️ Aktive Birdhouse-Knoten",
        "sensor_map_caption": "Nur Knoten mit relevanten lokalen Signalen (sensor_score > Schwelle) werden markiert.",
        "forecast_title": "🔮 Prognose-Horizont",
        "forecast_caption": "Ein einfacher, erklärbarer Indikator basierend auf Trend + Annahmen.",
        "proximity_title": "🚒 Nähe (Einsatzkontext)",
        "proximity_caption": "Operativ: Entfernung & geschätzte Anfahrtszeit zur nächsten Feuerwehr.",
        "alerts_title": "🔔 Warnungen",
        "alerts_caption": "Handlungsrelevante Warnungen aus Klima-Trend + Sensoren + Fusion.",
        "subscribe": "Warnungen abonnieren",
        "subscribe_hint": "Demo: Speichert nur die Auswahl in session_state (keine Emails).",
        "on": "AN",
        "off": "AUS",
        "fusion": "Fusions-Score",
        "final_level": "🔥 ENDSTUFE",
        "kpi_cells": "Rasterzellen",
        "kpi_hi": "Hoch / Extrem",
        "kpi_avg": "Ø Risikoscore",
        "kpi_date": "Datum",
        "legend": "🎨 Legende",
        "delta_legend": "🎨 Δ-Risiko Legende",
        "compare_hint": "Noch kein Szenario. Gehe zum Szenario-Tab und starte es.",
        "run_scenario": "Szenario ausführen",
        "run": "Start",
        "scenario_title": "🧪 Was-wäre-wenn Analyse (Szenario)",
        "scenario_text": "Simuliere Klima-Szenarien und bewerte den Einfluss auf das Waldbrandrisiko.",
        "map_title": "🗺️ Räumliches Waldbrandrisiko",
        "state_title": "🏛️ Risiko nach Bundesland",
        "decision_title": "🧠 Entscheidung & Interpretation",
        "auto_explain": "🧠 Auto-Erklärung",
        "sensor_timeline": "⏱️ Sensor-Risiko-Zeitverlauf",
        "trend_title": "⏱️ Trend (letzte Tage)",
        "trend_empty": "Trend erscheint, sobald mehrere Tage verfügbar sind.",
        "dir": "ltr",

        # NEW: Academic / concept text (DE)
        "concept_block_title": "Konzeptübersicht",
        "concept_block_text": (
            "Das KI-Entscheidungsmodul ist die operative Schicht, die heterogene Evidenz in eine handlungsfähige "
            "Waldbrand-Entscheidung überführt. Es bündelt (i) **klimabasierte räumliche Risiken** aus Rasterdaten, "
            "(ii) **Ground-Truth-Bestätigung** durch Birdhouse-Sensorknoten und (iii) **Entscheidungsunterstützung** "
            "wie Trend, Hotspots und Einsatznähe. Daraus entsteht eine transparente Pipeline: **beobachten → fusionieren "
            "→ interpretieren → handeln**."
        ),
        "map_concept_title": "Warum es eine Karte gibt",
        "map_concept_text": (
            "Die räumliche Karte liefert Lagebild und Priorisierung: Sie zeigt, wo Risiko konzentriert ist, wie es sich "
            "verteilt und welche Bereiche operative Schwellen überschreiten. Das unterstützt Monitoring und Einsatzplanung."
        ),
        "summary_concept_title": "Wie die Endstufe entsteht",
        "summary_concept_text": (
            "Die Endstufe basiert auf einem **Fusions-Score**, der das Klimasignal (modellbasiert) mit der stärksten "
            "Sensorbestätigung (lokale Evidenz) kombiniert. Dieses Design reduziert Fehlalarme und erhöht Vertrauen: "
            "bei hohem Klimarisiko ohne lokale Bestätigung bleibt die Eskalation konservativ; bei Übereinstimmung erfolgt "
            "eine klare Eskalation."
        ),
        "why_sensor_map_title": "Warum Birdhouse-Karte und Tabelle hier sind",
        "why_sensor_map_text": (
            "Birdhouse-Karte und Tabelle liefern nachvollziehbare Ground-Truth-Evidenz. Sie zeigen, welche Knoten relevante "
            "Signale beitragen, wo sie liegen und welche Indikatoren gemessen werden (z. B. PM2.5, RH, Temperatur). "
            "Das unterstützt Auditierbarkeit und operative Entscheidungen (z. B. Vor-Ort-Checks)."
        ),
        "forecast_explain_title": "Was die Prognose aussagt",
        "forecast_explain_text": (
            "Die Prognose ist ein erklärbarer Indikator aus der Entwicklung der letzten Tage. Sie ersetzt nicht das Modell, "
            "sondern kommuniziert, ob Bedingungen innerhalb des gewählten Horizonts *steigen*, *fallen* oder *stabil* sind."
        ),
        "proximity_explain_title": "Warum Nähe berücksichtigt wird",
        "proximity_explain_text": (
            "Nähe ergänzt operative Rahmenbedingungen: Gleiches Risiko kann je nach erwarteter Anfahrtszeit unterschiedliche "
            "Folgen haben. Die Distanz- und ETA-Schätzung unterstützt Bereitschaft und Ressourcen-Vorpositionierung."
        ),
        "alerts_explain_title": "Warum Warnungen generiert werden",
        "alerts_explain_text": (
            "Warnungen übersetzen Analytik in Handlung. Sie verdichten Eskalationen aus Trend, Sensoranomalien und "
            "Fusionsschwellen zu einer kurzen, entscheidungsreifen Liste."
        ),
    },
    "العربية": {
        "title": "🧩 محرك القرار الذكي",
        "subtitle": "تنبؤ مناخي • تأكيد حساسات • دعم قرار",
        "controls": "⚙️ التحكم",
        "date": "📅 التاريخ",
        "risk_level": "🔥 مستوى الخطر",
        "map_settings": "🗺️ إعدادات الخريطة",
        "view_mode": "وضع العرض",
        "risk_thr": "عتبة الخطر",
        "radius": "نصف قطر التجمع (كم)",
        "min_pts": "الحد الأدنى للنقاط",
        "tabs": ["🗺️ الخريطة", "🧠 ملخص القرار", "🏛️ الولايات", "🧪 سيناريو", "⚖️ مقارنة"],
        "scenario_inactive": "🟡 السيناريو غير مفعّل — شغّل سيناريو لتفعيل المقارنة",
        "scenario_active": "🟢 السيناريو مفعّل — المقارنة جاهزة",
        "no_sensors": "لا توجد بيانات حساسات.",
        "sensor_map_title": "🗺️ عقد Birdhouse النشطة",
        "sensor_map_caption": "نُظهر فقط العقد ذات الإشارات المهمة (sensor_score > العتبة).",
        "forecast_title": "🔮 التنبؤ المستقبلي",
        "forecast_caption": "مؤشر تنبؤ بسيط وشفاف يعتمد على الاتجاه الأخير + افتراضات.",
        "proximity_title": "🚒 القرب من محطة الإطفاء",
        "proximity_caption": "سياق تشغيلي: المسافة وزمن الاستجابة المتوقع لأقرب محطة.",
        "alerts_title": "🔔 التنبيهات",
        "alerts_caption": "تنبيهات عملية مبنية على الاتجاه المناخي + الحساسات + الدمج.",
        "subscribe": "اشتراك بالتنبيهات",
        "subscribe_hint": "عرض تجريبي: يخزن الاختيار فقط (بدون إرسال بريد).",
        "on": "تشغيل",
        "off": "إيقاف",
        "fusion": "درجة الدمج",
        "final_level": "🔥 المستوى النهائي",
        "kpi_cells": "عدد الخلايا",
        "kpi_hi": "عالي / شديد جدًا",
        "kpi_avg": "متوسط الخطر",
        "kpi_date": "التاريخ",
        "legend": "🎨 دليل الألوان",
        "delta_legend": "🎨 دليل فرق الخطر Δ",
        "compare_hint": "لا يوجد سيناريو بعد. اذهب لتبويب السيناريو وشغّله.",
        "run_scenario": "تشغيل سيناريو",
        "run": "تشغيل",
        "scenario_title": "🧪 تحليل ماذا لو؟",
        "scenario_text": "حاكي سيناريوهات مناخية وافحص تأثيرها على خطر الحريق.",
        "map_title": "🗺️ الخطر المكاني",
        "state_title": "🏛️ الخطر حسب الولاية",
        "decision_title": "🧠 القرار النهائي والتفسير",
        "auto_explain": "🧠 تفسير تلقائي",
        "sensor_timeline": "⏱️ خط زمني لخطر الحساسات",
        "trend_title": "⏱️ الاتجاه (آخر أيام)",
        "trend_empty": "سيظهر الاتجاه عند توفر أكثر من يوم.",
        "dir": "rtl",

        # NEW: Academic / concept text (AR)
        "concept_block_title": "نظرة مفاهيمية",
        "concept_block_text": (
            "محرك القرار هو الطبقة التشغيلية التي تحول الأدلة المتنوعة إلى قرار عملي لمخاطر الحرائق. يجمع بين "
            "(1) **خطر مكاني مبني على المناخ** من بيانات شبكية، (2) **تأكيد ميداني (Ground Truth)** من عقد Birdhouse، "
            "و(3) **دعم قرار** مثل الاتجاه والبؤر الساخنة وقرب الاستجابة. النتيجة خط قرار شفاف: "
            "**نرصد → ندمج → نفسّر → نتحرك**."
        ),
        "map_concept_title": "لماذا نعرض خريطة",
        "map_concept_text": (
            "الخريطة تقدم وعيًا مكانيًا واضحًا: أين يتركز الخطر وكيف يتوزع، وأي مناطق تتجاوز العتبات التشغيلية. "
            "هذا يساعد على تحديد الأولويات للمراقبة وتوزيع الموارد."
        ),
        "summary_concept_title": "كيف ننتج القرار النهائي",
        "summary_concept_text": (
            "القرار النهائي يعتمد على **درجة دمج** تجمع إشارة المناخ (خطر مبني على النموذج) مع أقوى تأكيد من الحساسات "
            "(دليل محلي). هذا يقلل الإنذارات الكاذبة ويرفع الثقة: إذا كان الخطر المناخي مرتفعًا لكن الحساسات هادئة "
            "تبقى الاستجابة محافظة؛ وإذا اتفقت الإشارتان يصير التصعيد حاسمًا."
        ),
        "why_sensor_map_title": "لماذا خريطة وجدول Birdhouse هنا",
        "why_sensor_map_text": (
            "خريطة وجدول Birdhouse يقدمان دليلًا ميدانيًا قابلًا للتتبع: أي عقدة ساهمت بإشارة مهمة، أين موقعها، "
            "وما هي القياسات (مثل PM2.5 والرطوبة والحرارة). هذا مهم للتدقيق ولاتخاذ قرار إرسال فرق فحص."
        ),
        "forecast_explain_title": "ماذا يعني التنبؤ",
        "forecast_explain_text": (
            "التنبؤ هنا مؤشر بسيط وشفاف مبني على تغير الخطر خلال الأيام الأخيرة. لا يستبدل النموذج، لكنه يوضح "
            "هل الخطر *يرتفع* أو *ينخفض* أو *مستقر* خلال الأفق المختار."
        ),
        "proximity_explain_title": "لماذا نضيف القرب",
        "proximity_explain_text": (
            "القرب يضيف بُعدًا تشغيليًا: نفس مستوى الخطر قد يكون أخطر في المناطق بعيدة الاستجابة. تقدير المسافة وزمن "
            "الوصول يساعد على الجاهزية وتوزيع الموارد قبل التصعيد."
        ),
        "alerts_explain_title": "لماذا نولد تنبيهات",
        "alerts_explain_text": (
            "التنبيهات تحول التحليل إلى أفعال. هي تلخص أهم التصعيدات الناتجة عن اتجاه الولايات وإشارات الحساسات وعتبات "
            "الدمج، بدل ترك المستخدم أمام بيانات خام كثيرة."
        ),
    }
}

# ============================================================
# SIDEBAR (Unified)
# ============================================================
with st.sidebar:
    lang = st.selectbox("🌐 Language", list(LANGS.keys()))
    T = LANGS[lang]

    st.divider()
    st.markdown("### 🧭 Navigation")
    cnav1, cnav2 = st.columns(2)
    with cnav1:
        if st.button("🧠 AI Hub", use_container_width=True):
            try:
                st.switch_page("pages/1_AI_Hub.py")
            except Exception:
                st.warning("AI Hub page path not found.")
    with cnav2:
        if st.button("🌲 Hardware", use_container_width=True):
            try:
                st.switch_page("pages/2_Hardware.py")
            except Exception:
                st.warning("Hardware page path not found.")

    st.divider()
    st.markdown(f"### {T['controls']}")

# ============================================================
# STYLING (Unified Dark Premium)
# ============================================================
st.markdown(f"""
<style>
/* ====== GLOBAL ====== */
.main {{
  direction: {T['dir']};
  text-align: {'right' if T['dir']=='rtl' else 'left'};
  background-color: #EAF4EC; /* تغيير الخلفية لتناسب النمط العام */
}}

/* ====== SECTION TITLE (عناوين الأقسام) ====== */
.section-title {{
  border: 1px solid #FF8C00;
  background: rgba(255, 140, 0, 0.1);
  border-radius: 14px;
  padding: .55rem .9rem;
  margin: 1rem 0 .75rem 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #000000; /* تغيير العنوان للأسود */
  display: inline-block;
}}

/* ====== CARDS (ألوانك الأصلية مع نصوص سوداء) ====== */
.status-card {{
  background: rgba(251, 146, 60, 0.15); /* لونك الأصلي */
  backdrop-filter: blur(12px);
  padding: 18px 18px;
  border-radius: 16px;
  border: 1px solid #f97316;
  margin: 12px 0;
  color: #000000 !important;
}}

.kpi-wrap {{
  background: rgba(234, 88, 12, 0.1); /* لونك الأصلي */
  border: 1px solid rgba(251, 146, 60, 0.4);
  border-radius: 16px;
  padding: 12px 14px;
  color: #000000 !important;
}}

/* ضمان أن كل النصوص داخل الكروت سوداء */
.status-card *, .kpi-wrap *, .legend-box * {{
  color: #000000 !important;
}}

.small-muted {{
  color: #475569; /* جعلها أغمق قليلاً لتظهر فوق الخلفية الفاتحة */
  font-size: 0.92rem;
}}

/* ====== SIDEBAR (أخضر وكتابة بيضاء صريحة) ====== */
section[data-testid="stSidebar"] {{
  background-color: #0F3D2E !important;
  border-right: 4px solid #FF8C00;
}}

/* إجبار كل نصوص السايد بار على اللون الأبيض */
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {{
  color: #FFFFFF !important;
  font-weight: 600 !important;
}}

/* تنسيق حقول الإدخال داخل السايد بار */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {{
  color: #000000 !important;
  background-color: #ffffff !important;
  border-radius: 8px;
}}

/* مستطيل اللغات والـ Selectbox داخل السايد بار */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
  background-color: #FF8C00 !important;
  border: none !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
  color: #000000 !important; /* النص المختار داخل المربع أسود */
  font-weight: 800 !important;
}}

.legend-box {{
  background: rgba(251, 146, 60, 0.15); 
  backdrop-filter: blur(10px);
  border-radius: 14px;
  padding: .8rem 1rem;
  border: 1px solid #f97316;
  color: #000000;
}}

/* ====== LEGEND COLOR FIX ====== */
.legend-box span {{s
  font-weight: 900;
}} 


</style>
""", unsafe_allow_html=True)

def section(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]
PARQUET_PATH = BASE_DIR / "daily_risk.parquet"
STATES_PATH = BASE_DIR / "data" / "germany_states.geojson"
SENSOR_DATA_PATH = BASE_DIR / "data" / "sensor_readings.csv"

# ============================================================
# OPTIONAL IMPORTS (components) + FALLBACKS
# ============================================================
# --- MAPS (optional) ---
try:
    from nexus_ai.components.maps import render_point_risk_map, render_hex_risk_map
except Exception:
    render_point_risk_map = None
    render_hex_risk_map = None

# --- STATE RISK (optional) ---
try:
    from nexus_ai.components.state_risk import load_states, compute_state_risk, render_state_risk_map
except Exception:
    load_states = None
    compute_state_risk = None
    render_state_risk_map = None

# --- TREND (optional) ---
try:
    from nexus_ai.components.trend_analysis import compute_state_trend
except Exception:
    compute_state_trend = None

# --- ALERTS (optional) ---
try:
    from nexus_ai.components.alerts import generate_alerts
except Exception:
    generate_alerts = None

# --- AUTO EXPLAIN (optional) ---
try:
    from nexus_ai.components.auto_explain import generate_risk_explanation
except Exception:
    generate_risk_explanation = None

# --- SCENARIO (optional) ---
try:
    from nexus_ai.components.scenario_simulator import render_scenario_simulator
except Exception:
    render_scenario_simulator = None

# --- COMPARE (optional) ---
try:
    from nexus_ai.components.compare_scenario import render_compare_map
except Exception:
    render_compare_map = None

# --- SENSORS (optional) ---
try:
    from nexus_ai.components.sensor_nodes import load_sensor_data, render_sensor_nodes_map
except Exception:
    load_sensor_data = None
    render_sensor_nodes_map = None

try:
    from nexus_ai.components.sensor_alerts import generate_sensor_alerts
except Exception:
    generate_sensor_alerts = None

try:
    from nexus_ai.components.fusion_engine import compute_fusion_score, fusion_level
except Exception:
    compute_fusion_score = None
    fusion_level = None


# ============================================================
# FALLBACK UTILS
# ============================================================
def load_parquet_safe(path: Path) -> tuple[pd.DataFrame, str]:
    if not path.exists():
        st.error(f"Missing parquet file: {path}")
        return pd.DataFrame(), "date"
    df = pd.read_parquet(str(path))
    date_col = "date" if "date" in df.columns else ("time" if "time" in df.columns else None)
    if date_col is None:
        st.error("Parquet missing a date/time column (expected 'date' or 'time').")
        return pd.DataFrame(), "date"
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    if "risk_level" not in df.columns:
        df["risk_level"] = "unknown"
    if "risk_score" not in df.columns:
        st.error("Parquet missing 'risk_score' column.")
        return pd.DataFrame(), date_col
    return df, date_col

def compute_sensor_score_row(row) -> float:
    score = 0.0
    pm25 = float(row.get("pm25", 0) or 0)
    rh = float(row.get("rh", 100) or 100)
    temp = float(row.get("temp_c", 0) or 0)

    if pm25 > 50:
        score += 0.45
    if rh < 30:
        score += 0.35
    if temp > 30:
        score += 0.25
    return float(min(score, 1.0))

def simple_fusion_score(climate_risk_0_1: float, sensor_risk_0_1: float | None) -> float:
    # fallback fusion if fusion_engine missing
    if sensor_risk_0_1 is None:
        return float(np.clip(climate_risk_0_1, 0, 1))
    return float(np.clip(0.65 * climate_risk_0_1 + 0.35 * sensor_risk_0_1, 0, 1))

def simple_fusion_level(fusion_0_1: float) -> str:
    if fusion_0_1 >= 0.80:
        return "EXTREME"
    if fusion_0_1 >= 0.60:
        return "HIGH"
    if fusion_0_1 >= 0.30:
        return "MEDIUM"
    return "LOW"

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    p1 = math.radians(lat1); p2 = math.radians(lat2)
    d1 = math.radians(lat2 - lat1)
    d2 = math.radians(lon2 - lon1)
    a = math.sin(d1/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(d2/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def trend_from_series(values: list[float]) -> str:
    # very simple direction for forecast indicator
    if len(values) < 3:
        return "stable"
    x = np.arange(len(values), dtype=float)
    y = np.array(values, dtype=float)
    # slope via polyfit
    slope = np.polyfit(x, y, 1)[0]
    if slope > 0.005:
        return "up"
    if slope < -0.005:
        return "down"
    return "stable"

# ============================================================
# HEADER
# ============================================================
st.title(T["title"])
st.markdown(f"<p class='small-muted'>{T['subtitle']}</p>", unsafe_allow_html=True)

# NEW: Academic concept overview (added, no design changes)
section(f"📌 {T['concept_block_title']}")
st.markdown("<div class='status-card'>", unsafe_allow_html=True)
st.markdown(T["concept_block_text"])
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ============================================================
# LOAD DATA
# ============================================================
df, date_col = load_parquet_safe(PARQUET_PATH)
if df.empty:
    st.stop()

all_dates = sorted(df[date_col].dt.date.unique())
default_idx = max(0, len(all_dates) - 1)

# ============================================================
# SIDEBAR CONTROLS (Unified)
# ============================================================
with st.sidebar:
    selected_date = st.selectbox(T["date"], all_dates, index=default_idx)

    levels = ["all"] + sorted(df["risk_level"].astype(str).unique())
    selected_level = st.selectbox(T["risk_level"], levels)

    st.divider()
    st.markdown(f"### {T['map_settings']}")
    map_mode = st.radio(T["view_mode"], ["Points", "Hex"], horizontal=True)

    st.divider()
    score_threshold = st.slider(T["risk_thr"], 0.5, 0.95, 0.7, 0.05)
    eps_km = st.slider(T["radius"], 10, 80, 25, 5)
    min_samples = st.slider(T["min_pts"], 3, 30, 10, 1)

    st.divider()
    # Alerts subscription demo toggle
    if "subscribed_alerts" not in st.session_state:
        st.session_state.subscribed_alerts = False

    sub_label = f"🔔 {T['subscribe']} ({T['on'] if st.session_state.subscribed_alerts else T['off']})"
    if st.button(sub_label, use_container_width=True):
        st.session_state.subscribed_alerts = not st.session_state.subscribed_alerts
        st.toast(T["subscribe_hint"])
        st.rerun()

# ============================================================
# FILTER DATA (day + level)
# ============================================================
df_day = df[df[date_col].dt.date == selected_date].copy()
if selected_level != "all":
    df_day = df_day[df_day["risk_level"].astype(str) == str(selected_level)].copy()

# yesterday
yesterday_df = None
idx = all_dates.index(selected_date)
if idx > 0:
    yday = all_dates[idx - 1]
    yesterday_df = df[df[date_col].dt.date == yday].copy()

# ============================================================
# KPIs (Unified)
# ============================================================
with st.container():
    st.markdown('<div class="kpi-wrap">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(T["kpi_cells"], len(df_day))
    c2.metric(T["kpi_hi"], int((df_day["risk_level"].isin(["high", "extreme"])).sum()) if "risk_level" in df_day.columns else 0)
    c3.metric(T["kpi_avg"], round(float(df_day["risk_score"].mean()) if not df_day.empty else 0.0, 3))
    c4.metric(T["kpi_date"], str(selected_date))
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ============================================================
# SCENARIO STATUS INDICATOR
# ============================================================
scenario_risk = st.session_state.get("scenario_risk_score", None)
if scenario_risk is None:
    st.warning(T["scenario_inactive"])
else:
    st.success(T["scenario_active"])

# ============================================================
# STATES + TREND + ALERTS (if components exist)
# ============================================================
states_trend = None
state_alerts = []

if load_states and compute_state_risk and compute_state_trend:
    try:
        states_gdf = load_states(STATES_PATH)
        states_today = compute_state_risk(df_day, states_gdf)
        states_yday = compute_state_risk(yesterday_df, states_gdf) if yesterday_df is not None else None
        states_trend = compute_state_trend(states_today, states_yday)

        if generate_alerts:
            state_alerts = generate_alerts(states_trend, None)  # second arg kept as None (as your original)
        else:
            # fallback: simple alert summary
            top = states_trend.sort_values("mean_risk", ascending=False).head(3)
            state_alerts = [f"State escalation focus: {', '.join(top['NAME_1'].astype(str).tolist())}"]
    except Exception as e:
        state_alerts = [f"State trend failed: {e}"]
else:
    # fallback if state components missing
    state_alerts = ["State module unavailable (components/state_risk or trend_analysis not connected)."]

# ============================================================
# SENSORS
# ============================================================
df_sensors = pd.DataFrame()
sensor_alerts = []

if SENSOR_DATA_PATH.exists():
    try:
        if load_sensor_data:
            df_sensors = load_sensor_data(str(SENSOR_DATA_PATH))
            # normalize column names if needed
            df_sensors.columns = [c.lower() for c in df_sensors.columns]
        else:
            df_sensors = pd.read_csv(str(SENSOR_DATA_PATH))
            df_sensors.columns = [c.lower() for c in df_sensors.columns]
        df_sensors["sensor_score"] = df_sensors.apply(compute_sensor_score_row, axis=1)

        if generate_sensor_alerts:
            sensor_alerts = generate_sensor_alerts(df_sensors)
        else:
            # fallback alerts
            mx = float(df_sensors["sensor_score"].max()) if not df_sensors.empty else 0.0
            if mx >= 0.75:
                sensor_alerts = [f"Critical sensor escalation detected (score={mx:.2f})"]
            elif mx >= 0.55:
                sensor_alerts = [f"Moderate sensor escalation detected (score={mx:.2f})"]
            else:
                sensor_alerts = ["No significant sensor escalation detected."]
    except Exception as e:
        df_sensors = pd.DataFrame()
        sensor_alerts = [f"Sensor load failed: {e}"]
else:
    sensor_alerts = [T["no_sensors"]]

# ============================================================
# TABS
# ============================================================
tab_map, tab_summary, tab_state, tab_scenario ,  tab_compare = st.tabs(T["tabs"])

# ============================================================
# TAB: MAP
# ============================================================
with tab_map:

    st.markdown("""
    <div class="status-card">
    <b>Concept:</b> This map represents the spatial distribution of wildfire risk derived from
    climate-driven AI models. Each cell is an independent risk estimation unit, forming the
    baseline layer of the NEXUS decision system.
    </div>
    """, unsafe_allow_html=True)

    section(T["map_title"])

    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    if render_point_risk_map and render_hex_risk_map:
        if map_mode == "Hex" and len(df_day) >= 300:
            render_hex_risk_map(df_day, selected_date)
        else:
            render_point_risk_map(df_day, selected_date)
    else:
        lat_col = next((c for c in df_day.columns if c.lower() in ["lat", "latitude"]), None)
        lon_col = next((c for c in df_day.columns if c.lower() in ["lon", "long", "longitude"]), None)

        if lat_col and lon_col and not df_day.empty:
            tmp = df_day.rename(columns={lat_col: "lat", lon_col: "lon"}).copy()
            tmp = tmp[["lat", "lon", "risk_score"]].dropna()
            st.map(tmp, zoom=6)
            st.caption("Fallback map (components/maps.py not connected yet).")
        else:
            st.warning("Map unavailable: missing lat/lon columns or empty dataset.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"#### {T['legend']}")
    st.markdown("""
    <div class="legend-box">
        <span style="color:#16A34A">●</span> Low — score &lt; 0.30<br>
        <span style="color:#FACC15">●</span> Medium — 0.30 – 0.60<br>
        <span style="color:#EF4444">●</span> High — 0.60 – 0.80<br>
        <span style="color:#7C3AED">●</span> Extreme — &gt; 0.80
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ============================================================
# TAB: DECISION SUMMARY (FINAL – CLEAN + STABLE)
# ============================================================
with tab_summary:

    section(T["decision_title"])

    st.markdown("""
    <div class="status-card">
    <b>Decision Layer Concept:</b>
    This layer fuses climate risk with ground-truth sensor confirmation
    to produce a single explainable operational decision.
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # FUSION SCORE
    # -----------------------------
    climate_raw = float(df_day["risk_score"].mean()) if not df_day.empty else 0.0
    climate_score = float(np.clip(climate_raw, 0, 1))
    sensor_score = float(df_sensors["sensor_score"].max()) if not df_sensors.empty else None

    fusion = compute_fusion_score(climate_score, sensor_score) if compute_fusion_score else simple_fusion_score(climate_score, sensor_score)
    level = fusion_level(fusion) if fusion_level else simple_fusion_level(fusion)

    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Climate Score", round(climate_score, 2))
    c2.metric("Sensor Score", "-" if sensor_score is None else round(sensor_score, 2))
    c3.metric("Fusion Score", round(fusion, 2))
    st.markdown(f"### 🔥 FINAL LEVEL: **{level}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # SENSOR MAP (GUARANTEED TO SHOW)
    # ============================================================
    section(T["sensor_map_title"])
    st.caption(T["sensor_map_caption"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    if df_sensors.empty:
        st.warning("No sensor data available.")
        df_map = pd.DataFrame()
    else:
        df_map = df_sensors.copy()

        lat_col = next((c for c in df_map.columns if c.lower() in ["lat", "latitude"]), None)
        lon_col = next((c for c in df_map.columns if c.lower() in ["lon", "longitude", "long"]), None)

        if not lat_col or not lon_col:
            st.error(f"Sensor data missing lat/lon columns. Found: {list(df_map.columns)}")
            df_map = pd.DataFrame()
        else:
            df_map = df_map.rename(columns={lat_col: "lat", lon_col: "lon"})
            df_map["lat"] = pd.to_numeric(df_map["lat"], errors="coerce")
            df_map["lon"] = pd.to_numeric(df_map["lon"], errors="coerce")
            df_map = df_map.dropna(subset=["lat", "lon"])

            if df_map.empty:
                st.error("All sensor locations are invalid.")
            else:
                st.map(df_map[["lat", "lon"]], zoom=7)

                if render_sensor_nodes_map:
                    with st.expander("Enhanced sensor visualization"):
                        render_sensor_nodes_map(df_map)

                cols = [c for c in ["device_id", "sensor_score", "pm25", "temp_c", "rh", "battery_v", "rssi"] if c in df_map.columns]
                if cols:
                    st.dataframe(df_map[cols].reset_index(drop=True), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # FORECAST
    # ============================================================
    section(T["forecast_title"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    df_hist = df.copy()
    df_hist["d"] = df_hist[date_col].dt.date
    hist = df_hist.groupby("d")["risk_score"].mean().tail(7)

    if len(hist) > 1:
        st.line_chart(hist)
    else:
        st.info(T["trend_empty"])

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # PROXIMITY
    # ============================================================
    section(T["proximity_title"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    if not df_map.empty:
        ref_lat = df_map["lat"].mean()
        ref_lon = df_map["lon"].mean()
    else:
        ref_lat = ref_lon = None

    if ref_lat is None:
        st.info("No reference point available.")
    else:
        stations = pd.DataFrame([
            {"station": "Feuerwehr Köln", "lat": 50.9375, "lon": 6.9603},
            {"station": "Feuerwehr Bonn", "lat": 50.7374, "lon": 7.0982},
            {"station": "Feuerwehr Düsseldorf", "lat": 51.2277, "lon": 6.7735},
        ])

        stations["dist_km"] = stations.apply(lambda r: haversine_km(ref_lat, ref_lon, r["lat"], r["lon"]), axis=1)
        nearest = stations.sort_values("dist_km").iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Nearest Station", nearest["station"])
        c2.metric("Distance", f"{nearest['dist_km']:.1f} km")
        c3.metric("ETA", f"{int(nearest['dist_km']/45*60)} min")

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # ALERTS
    # ============================================================
    section(T["alerts_title"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    alerts = []
    alerts.extend(state_alerts)
    alerts.extend(sensor_alerts)

    if fusion >= 0.8:
        alerts.insert(0, "🔴 Critical fusion escalation")
    elif fusion >= 0.6:
        alerts.insert(0, "🟠 Elevated fusion escalation")
    else:
        alerts.insert(0, "🟢 Normal conditions")

    for a in alerts[:10]:
        st.info(a)

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # AUTO EXPLANATION
    # ============================================================
    section(T["auto_explain"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    if generate_risk_explanation:
        st.markdown(generate_risk_explanation(selected_date, states_trend, None, alerts))
    else:
        st.markdown("- Decision is based on climate + sensor fusion.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB: STATES
# ============================================================
with tab_state:
    section(T["state_title"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)

    if states_trend is None:
        st.warning("No state trend available.")
    else:
        if render_state_risk_map:
            render_state_risk_map(states_trend)
        st.dataframe(states_trend.drop(columns=["geometry"], errors="ignore"), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB: SCENARIO
# ============================================================
with tab_scenario:
    section(T["scenario_title"])
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.markdown(T["scenario_text"])

    if render_scenario_simulator:
        render_scenario_simulator()
    else:
        base = float(np.clip(climate_raw, 0, 1))
        delta = st.slider("Δ climate risk", -0.3, 0.3, 0.0, 0.01)
        if st.button(T["run_scenario"]):
            st.session_state["scenario_risk_score"] = float(np.clip(base + delta, 0, 1))
            st.success("Scenario updated.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TAB: COMPARE
# ============================================================
with tab_compare:
    section("⚖️ Real Risk vs Scenario Comparison")

    scenario_risk = st.session_state.get("scenario_risk_score", None)
    if scenario_risk is None:
        st.warning(T["compare_hint"])
    else:
        st.markdown("<div class='status-card'>", unsafe_allow_html=True)

        if render_compare_map:
            scenario_df = df_day.copy()
            scenario_df["risk"] = scenario_risk
            delta_df = render_compare_map(df_day, scenario_df)

            c1, c2, c3 = st.columns(3)
            c1.metric("Mean Δ Risk", round(delta_df["delta"].mean(), 2))
            c2.metric("Max Increase", round(delta_df["delta"].max(), 2))
            c3.metric("Max Decrease", round(delta_df["delta"].min(), 2))
        else:
            delta = scenario_risk - climate_score
            st.metric("Scenario Δ", f"{delta:+.2f}")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("© 2026 NEXUS AI Systems | AI Decision Engine")


            
