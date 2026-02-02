import base64
from pathlib import Path
import streamlit as st

def img_to_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()

def load_css():
    # --- كود البحث عن اللوجو وتحديده ---
    current_dir = Path(__file__).parent if Path(__file__).parent.name != "pages" else Path(__file__).parent.parent
    logo_path = current_dir / "assets" / "firesense_logo.png"
    
    # عرض اللوجو والاسم بتنسيق متراص وكبير
    if logo_path.exists():
        try:
            logo_base64 = img_to_base64(str(logo_path))
            st.sidebar.markdown(
                f"""
                <div style="text-align: center; margin-top: -40px;">
                    <img src="data:image/png;base64,{logo_base64}" width="380" style="margin-bottom: 0px;">
                    <h1 style="color: white !important; font-size: 35px !important; font-weight: 900 !important; margin-top: -20px; margin-bottom: 0px; letter-spacing: 1px;">
                        NEXUS AI
                    </h1>
                    <p style="color: #FF8C00 !important; font-size: 15px !important; font-weight: 700 !important; margin-top: -5px; margin-bottom: 15px;">
                        Wildfire Intelligence System
                    </p>
                    <hr style="border-top: 1px solid rgba(255,255,255,0.1); margin: 0 20px 20px 20px;">
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.sidebar.error(f"Error loading logo: {e}")

    # --- كود الـ CSS الأساسي المعدل لضبط المسافات والألوان ---
    # --- كود الـ CSS الكامل والمعدل لضمان ألوان الليجند ---
    st.markdown("""
    <style>
    /* ====== GLOBAL ====== */
    .stApp {
        background-color: #EAF4EC;
        font-family: Arial, sans-serif;
    }

    header[data-testid="stHeader"] { display: none; }
    div[data-testid="stToolbar"] { display: none; }

    /* ====== SIDEBAR GENERAL ====== */
    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F3D2E !important;
        border-right: 4px solid #FF8C00;
    }

    /* التعديل هنا: جعلنا اللون الأبيض لا يشمل عناصر الليجند */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p:not(.legend-text),
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span:not(.legend-color),
    section[data-testid="stSidebar"] div:not(.legend-box) {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* استهداف نصوص القوائم وأسماء الصفحات */
    section[data-testid="stSidebarNav"] span,
    section[data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
    }

    /* ====== SELECTBOX FIX (Language) ====== */
    div[data-baseweb="select"] > div:first-child {
        background-color: #FF8C00 !important;
        border-radius: 10px !important;
        border: none !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] p,
    div[data-baseweb="select"] div {
        color: #000000 !important;
        font-weight: 900 !important;
    }

    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    /* ====== LEGEND BOX FIX (التعديل الجديد والمهم) ====== */
    .legend-box {
        background: rgba(251, 146, 60, 0.15) !important; 
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: .8rem 1rem;
        border: 1px solid #f97316 !important;
        margin-bottom: 15px;
        display: block;
    }

    /* نضمن هنا أن الألوان داخل الليجند لا تتبع اللون الأبيض العام */
    .legend-box span.legend-color {
        all: unset !important; /* مسح أي تنسيق موروث */
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        display: inline-block;
        margin-right: 8px;
        /* سيأخذ اللون من خاصية style المباشرة في HTML */
    }

    .legend-box span.legend-text {
        color: #FFFFFF !important; /* نص الشرح أبيض */
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    /* ====== HERO & CARDS (كما هي بدون تغيير) ====== */
    .hero-wrap{
        width:100%; height:220px; border-radius:16px;
        overflow:hidden; margin-bottom:18px; position:relative;
    }
    .hero-wrap img{ width:100%; height:100%; object-fit:cover; display:block; }
    .hero-overlay{
        position:absolute; inset:0;
        background:linear-gradient(90deg, rgba(15,61,46,0.55), rgba(0,0,0,0.10));
    }
    .hero-text{
        position:absolute; left:22px; bottom:22px; color:white;
        font-size:24px; font-weight:900; text-shadow:0 2px 6px rgba(0,0,0,0.45);
    }
    .card {
        background: #FF8C00;
        padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #E67600; margin-bottom: 18px;
    }
    .card, .card * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    .stButton > button {
        background-color: #FF8C00 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important; font-weight: 800 !important;
    }
    hr { border-top: 2px solid #FF8C00; }
    </style>
    """, unsafe_allow_html=True)