import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="NEXUS – Wildfire Intelligence",
    page_icon="🔥",
    layout="wide"
)

load_css()

# قيم افتراضية
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "mode" not in st.session_state:
    st.session_state.mode = "Geo"

with st.sidebar:
    # لوغو مشروعك (مضمون)
    st.image("assets/firesense_logo.png", width=90)

    st.markdown("## NEXUS")
    st.caption("AI Wildfire Decision Platform")

    # اختيار اللغة (رح يصير اورانج من CSS)
    st.session_state.lang = st.selectbox(
        "🌐 Interface Language",
        ["English", "Deutsch", "العربية"],
        index=["English","Deutsch","العربية"].index(st.session_state.lang)
    )

    st.markdown("---")

    # وضع النظام
    st.session_state.mode = st.radio(
        "System Mode",
        ["Geo", "Manual"],
        index=0 if st.session_state.mode == "Geo" else 1
    )
st.switch_page("pages/1_AI_Hub.py")

