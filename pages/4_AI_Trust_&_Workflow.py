import streamlit as st
from pathlib import Path
import pandas as pd
from utils import img_to_base64, load_css

# استدعاء الـ CSS الأساسي من ملف utils
load_css()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NEXUS AI | Trust & Workflow",
    layout="wide",
    page_icon="🧩"
)

# ============================================================
# LANGUAGES (نفس بياناتك بدون تغيير)
# ============================================================
LANGS = {
    "English": {
        "dir": "ltr",
        "title": "🧩 AI Trust & Decision Workflow",
        "subtitle": "How NEXUS transforms data into explainable decisions",
        "arch": "System Architecture",
        "arch_txt": "This diagram illustrates the complete NEXUS intelligence pipeline. The architecture is layered to ensure transparency and trust.",
        "workflow": "Decision Workflow",
        "trust": "Why This Architecture Is Trustworthy",
        "points": [
            "Multiple independent data sources reduce single-point failure.",
            "Sensor data confirms or rejects satellite predictions.",
            "Fusion layer assigns confidence, not just risk.",
            "Decisions are explainable and traceable to inputs.",
            "System works even if one layer is missing."
        ]
    },
    "Deutsch": {
        "dir": "ltr",
        "title": "🧩 KI-Vertrauen & Entscheidungsworkflow",
        "subtitle": "Wie NEXUS Daten in erklärbare Entscheidungen umwandelt",
        "arch": "Systemarchitektur",
        "arch_txt": "Dieses Diagramm zeigt die vollständige NEXUS-Intelligenzkette. Die Architektur ist geschichtet, um Transparenz zu gewährleisten.",
        "workflow": "Entscheidungsworkflow",
        "trust": "Warum diese Architektur vertrauenswürdig ist",
        "points": [
            "Mehrere Datenquellen verhindern Einzelpunktfehler.",
            "Sensordaten bestätigen Satellitenvorhersagen.",
            "Die Fusionsebene bewertet Sicherheit, nicht nur Risiko.",
            "Entscheidungen sind erklärbar und rückverfolgbar.",
            "Das System funktioniert auch bei Teilausfällen."
        ]
    },
    "العربية": {
        "dir": "rtl",
        "title": "🧩 الثقة بالذكاء الاصطناعي وسير القرار",
        "subtitle": "كيف يحول نظام NEXUS البيانات إلى قرارات قابلة للتفسير",
        "arch": "المخطط المعماري للنظام",
        "arch_txt": "يوضح هذا المخطط سلسلة الذكاء الكاملة في نظام NEXUS لضمان الشفافية والمتانة والثقة.",
        "workflow": "سير اتخاذ القرار",
        "trust": "لماذا هذه المعمارية موثوقة",
        "points": [
            "مصادر بيانات متعددة تقلل الخطأ الفردي.",
            "البيانات الميدانية تؤكد أو تنفي التوقعات الفضائية.",
            "طبقة الدمج تعطي درجة ثقة وليس رقم فقط.",
            "القرار يمكن تفسيره وربطه بالمصادر.",
            "النظام يعمل حتى عند غياب بعض الطبقات."
        ]
    }
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    lang = st.selectbox("🌐 Language", list(LANGS.keys()))
    T = LANGS[lang]
    if st.button("⬅️ Back to AI Hub"):
        st.switch_page("pages/1_AI_Hub.py")

# ============================================================
# CSS CUSTOM (التنسيق المتفق عليه)
# ============================================================
st.markdown(f"""
<style>
/* ضبط الاتجاه حسب اللغة */
.stApp {{
    direction: {T['dir']};
    text-align: {'right' if T['dir']=='rtl' else 'left'};
}}

/* العناوين السوداء */
h1, h2, h3 {{
    color: #000000 !important;
    font-weight: 800 !important;
}}

/* ستايل الكروت البرتقالية الشفافة */
.status-card {{
    background: rgba(251, 146, 60, 0.15) !important; 
    backdrop-filter: blur(12px);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #f97316;
    margin-bottom: 20px;
    color: #000000 !important;
}}

/* إجبار أي نص داخل الكرت على اللون الأسود */
.status-card * {{
    color: #000000 !important;
}}

/* ستايل النجاح (النقاط الخضراء) لتناسب الخلفية الفاتحة */
div.stAlert {{
    background-color: rgba(15, 61, 46, 0.1);
    color: #0F3D2E;
    border: 1px solid #0F3D2E;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONTENT (مرتبة حسب طلبك)
# ============================================================

st.title(T["title"])
st.caption(T["subtitle"])

# SECTION: ARCHITECTURE
st.markdown("## " + T["arch"])
st.markdown(f"<div class='status-card'>{T['arch_txt']}</div>", unsafe_allow_html=True)

# المخطط المعماري
ARCH_IMG = Path(__file__).resolve().parents[1] / "assets" / "architecture_diagram.png"
if ARCH_IMG.exists():
    st.image(ARCH_IMG, caption="NEXUS Architecture", use_container_width=True)

# SECTION: ANALYSIS
st.markdown("## 📊 Evidence Contribution Analysis")
st.markdown("""
    <div class="status-card">
    This chart illustrates how different evidence layers contribute to the final decision.
    NEXUS balances multiple independent signals to ensure robust decisions.
    </div>
""", unsafe_allow_html=True)

confidence_df = pd.DataFrame({
    "Layer": ["Climate Models", "Satellite Data", "Field Sensors", "Historical Patterns"],
    "Contribution": [0.35, 0.25, 0.30, 0.10]
})
st.bar_chart(confidence_df.set_index("Layer"))

# SECTION: WORKFLOW
st.markdown("## " + T["workflow"])
st.markdown(f"""
    <div class='status-card'>
    <b>1. Data Ingestion:</b> Climate, satellite, and IoT sensors collection.<br><br>
    <b>2. AI Risk Estimation:</b> Generates spatial wildfire risk scores.<br><br>
    <b>3. Ground Truth:</b> Field sensors validate or correct predictions.<br><br>
    <b>4. Fusion:</b> Evidence layers combined into confidence scoring.<br><br>
    <b>5. Operational Output:</b> Alerts and maps generation.
    </div>
""", unsafe_allow_html=True)

# SECTION: TRUST
st.markdown("## " + T["trust"])
for p in T["points"]:
    st.success(p)

# FOOTER
st.divider()
st.caption("© 2026 NEXUS AI – Explainable Wildfire Intelligence")