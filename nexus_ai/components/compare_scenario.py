import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

DARK_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"


def render_compare_map(real_df: pd.DataFrame, scenario_df: pd.DataFrame):
    """
    real_df     : dataframe with lat, lon, risk_score
    scenario_df : dataframe with lat, lon, risk (scenario)
    """

    # ------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------
    required_real = {"risk_score"}
    if not required_real.issubset(real_df.columns):
        raise KeyError("real_df must contain 'risk_score' column")

    if "risk" not in scenario_df.columns:
        raise KeyError("scenario_df must contain 'risk' column")

    # detect lat/lon columns
    lat_col = next(c for c in real_df.columns if c.lower() in ["lat", "latitude"])
    lon_col = next(c for c in real_df.columns if c.lower() in ["lon", "longitude", "long"])

    # ------------------------------------------------------------
    # Merge real + scenario (row-aligned)
    # ------------------------------------------------------------
    df = real_df.copy().reset_index(drop=True)
    df["scenario_risk"] = scenario_df["risk"].values

    # ------------------------------------------------------------
    # Delta computation
    # ------------------------------------------------------------
    df["delta"] = df["scenario_risk"] - df["risk_score"]

    def delta_color(d):
        if d > 0.2:
            return [200, 0, 0, 180]      # much worse
        elif d > 0.05:
            return [255, 120, 0, 160]    # worse
        elif d < -0.2:
            return [0, 180, 0, 160]      # much better
        elif d < -0.05:
            return [120, 200, 0, 160]    # better
        else:
            return [150, 150, 150, 120]  # similar

    df["color"] = df["delta"].apply(delta_color)
    df["radius"] = np.clip(np.abs(df["delta"]), 0, 1) * 9000 + 3000

    # ------------------------------------------------------------
    # Map layer
    # ------------------------------------------------------------
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=[lon_col, lat_col],
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
    )

    view = pdk.ViewState(
        latitude=float(df[lat_col].mean()),
        longitude=float(df[lon_col].mean()),
        zoom=5.3,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style=DARK_STYLE,
        tooltip={
            "html": """
            <b>Δ Risk (Scenario − Real)</b><br/>
            Real: {risk_score}<br/>
            Scenario: {scenario_risk}<br/>
            Delta: {delta}
            """,
            "style": {"backgroundColor": "#111", "color": "white"},
        },
    )

    st.pydeck_chart(deck, use_container_width=True)

    return df
