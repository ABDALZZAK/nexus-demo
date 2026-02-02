import streamlit as st
import pydeck as pdk
import numpy as np
from sklearn.cluster import DBSCAN

DARK_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"


def detect_hotspots(df, score_threshold=0.7, eps_km=25, min_samples=10):
    if df.empty:
        return df.iloc[0:0].copy()

    lat_col = next((c for c in df.columns if c.lower() in ["lat", "latitude"]), None)
    lon_col = next((c for c in df.columns if c.lower() in ["lon", "long", "longitude"]), None)
    if lat_col is None or lon_col is None:
        raise ValueError("Latitude/Longitude columns not found in df.")
    if "risk_score" not in df.columns:
        raise ValueError("Column 'risk_score' not found in df.")

    dfh = df[df["risk_score"] >= score_threshold].dropna(subset=[lat_col, lon_col]).copy()
    if dfh.empty:
        return dfh

    # km -> degrees (approx): 1 deg ~ 111 km
    eps_deg = eps_km / 111.0

    coords = dfh[[lat_col, lon_col]].to_numpy()
    labels = DBSCAN(eps=eps_deg, min_samples=min_samples).fit_predict(coords)
    dfh["cluster"] = labels

    dfh = dfh[dfh["cluster"] != -1].copy()
    return dfh


def render_hotspots(df):
    if df.empty:
        st.info("No hotspots to show.")
        return

    lat_col = next((c for c in df.columns if c.lower() in ["lat", "latitude"]), None)
    lon_col = next((c for c in df.columns if c.lower() in ["lon", "long", "longitude"]), None)

    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=[lon_col, lat_col],
        get_fill_color=[255, 0, 0],
        get_radius=14000,
        opacity=0.6,
        pickable=True,
    )

    view = pdk.ViewState(
        latitude=float(df[lat_col].mean()),
        longitude=float(df[lon_col].mean()),
        zoom=5.3,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style=DARK_STYLE,
        tooltip={
            "html": "<b>Hotspot</b><br/>Cluster: {cluster}<br/>Score: {risk_score}",
            "style": {"backgroundColor": "#111", "color": "white"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True)
