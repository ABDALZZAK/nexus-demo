import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

# ==================================================
# Map Style
# ==================================================
DARK_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"

# ==================================================
# Risk colors for Point map
# ==================================================
RISK_COLORS = {
    "low": [0, 255, 127],
    "medium": [255, 215, 0],
    "high": [255, 69, 0],
    "extreme": [255, 0, 255],
}
DEFAULT_COLOR = [120, 120, 120]

# ==================================================
# Helpers
# ==================================================
def _find_lat_lon(df: pd.DataFrame):
    lat_col = next((c for c in df.columns if c.lower() in ["lat", "latitude"]), None)
    lon_col = next((c for c in df.columns if c.lower() in ["lon", "long", "longitude"]), None)
    return lat_col, lon_col


# ==================================================
# POINT MAP
# ==================================================
def render_point_risk_map(df: pd.DataFrame, date_label):
    if df.empty:
        st.warning("⚠️ No data available.")
        return

    lat_col, lon_col = _find_lat_lon(df)
    if lat_col is None or lon_col is None:
        st.error("Latitude / Longitude columns not found.")
        return

    df = df.dropna(subset=[lat_col, lon_col]).copy()

    # Thin points (keep high/extreme + sample others)
    if "risk_level" in df.columns:
        hi = df[df["risk_level"].isin(["high", "extreme"])]
        other = df[~df.index.isin(hi.index)]
        if len(other) > 2500:
            other = other.sample(2500, random_state=42)
        df = pd.concat([hi, other], ignore_index=True)

    # Color by risk level
    if "risk_level" in df.columns:
        df["color"] = df["risk_level"].astype(str).str.lower().apply(
            lambda x: RISK_COLORS.get(x, DEFAULT_COLOR)
        )
    else:
        df["color"] = [DEFAULT_COLOR] * len(df)

    # Radius by score
    if "risk_score" in df.columns:
        df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)
        df["radius"] = np.clip(df["risk_score"], 0, 1) * 8000 + 2000
    else:
        df["radius"] = 3500

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=[lon_col, lat_col],
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.85,
    )

    view_state = pdk.ViewState(
        latitude=float(df[lat_col].mean()),
        longitude=float(df[lon_col].mean()),
        zoom=5.3,
        pitch=0,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=DARK_STYLE,
        tooltip={
            "html": f"""
            <b>Risk level:</b> {{risk_level}}<br/>
            <b>Risk score:</b> {{risk_score}}<br/>
            <b>Date:</b> {date_label}
            """,
            "style": {"backgroundColor": "#111", "color": "white"},
        },
    )

    st.pydeck_chart(deck, use_container_width=True)


# ==================================================
# HEX MAP (FIXED VERSION)
# ==================================================
def render_hex_risk_map(df: pd.DataFrame, date_label):
    if df.empty:
        st.warning("⚠️ No data available.")
        return

    lat_col, lon_col = _find_lat_lon(df)
    if lat_col is None or lon_col is None:
        st.error("Latitude / Longitude columns not found.")
        return

    if "risk_score" not in df.columns:
        st.error("Column 'risk_score' not found. Hex map requires risk_score.")
        return

    # =========================
    # Clean & validate data
    # =========================
    df_hex = (
        df[[lat_col, lon_col, "risk_score"]]
        .apply(pd.to_numeric, errors="coerce")
        .dropna()
    )

    if df_hex.empty:
        st.warning("Not enough valid data to render hex aggregation.")
        return

    # =========================
    # View state
    # =========================
    view_state = pdk.ViewState(
        latitude=float(df_hex[lat_col].mean()),
        longitude=float(df_hex[lon_col].mean()),
        zoom=6.0,
        pitch=40,
    )

    # =========================
    # Hexagon layer
    # =========================
    layer = pdk.Layer(
        "HexagonLayer",
        data=df_hex,
        get_position=[lon_col, lat_col],
        radius=5000,               # 5 km (works well for Germany)
        elevation_scale=40,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=0.85,
        pickable=True,
        get_elevation_weight="risk_score",
        elevation_aggregation="MEAN",
        get_color_weight="risk_score",
        color_aggregation="MEAN",
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=DARK_STYLE,
        tooltip={
            "html": f"""
            <b>Mean risk:</b> {{elevationValue}}<br/>
            <b>Date:</b> {date_label}
            """,
            "style": {"backgroundColor": "#111", "color": "white"},
        },
    )

    st.pydeck_chart(deck, use_container_width=True)
