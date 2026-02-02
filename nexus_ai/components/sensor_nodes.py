import streamlit as st
import pandas as pd
import pydeck as pdk


# ============================================================
# Load sensor CSV
# ============================================================
@st.cache_data(show_spinner=False)
def load_sensor_data(csv_path: str) -> pd.DataFrame:
    """
    Loads Birdhouse sensor readings from CSV.
    Required columns:
    - device_id
    - lat, lon
    Optional:
    - pm25, temp_c, rh, battery_v, rssi, timestamp_utc
    """
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = [c.lower() for c in df.columns]

    required = {"device_id", "lat", "lon"}
    if not required.issubset(df.columns):
        raise ValueError(
            f"Sensor CSV must contain columns: {sorted(required)}"
        )

    if "timestamp_utc" in df.columns:
        df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce")

    return df


# ============================================================
# Render sensor node map
# ============================================================
def render_sensor_nodes_map(df: pd.DataFrame):
    """
    Displays Birdhouse nodes on a map with basic health tooltip.
    """

    if df.empty:
        st.info("No sensor nodes available.")
        return

    # Ensure required columns
    if not {"lat", "lon"}.issubset(df.columns):
        st.warning("Sensor data missing lat/lon.")
        return

    # Aggregate per device (latest reading)
    if "timestamp_utc" in df.columns:
        df = (
            df.sort_values("timestamp_utc")
            .groupby("device_id", as_index=False)
            .tail(1)
        )

    # Tooltip fields
    tooltip_fields = {
        "html": """
        <b>Birdhouse {device_id}</b><br/>
        PM2.5: {pm25} µg/m³<br/>
        Temp: {temp_c} °C<br/>
        RH: {rh} %<br/>
        Battery: {battery_v} V<br/>
        RSSI: {rssi} dBm
        """,
        "style": {"backgroundColor": "#111", "color": "white"}
    }

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_radius=120,
        pickable=True,
        auto_highlight=True,
        get_fill_color="[255, 80, 80]",
    )

    view = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=8,
        pitch=0,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip=tooltip_fields,
    )

    st.pydeck_chart(deck, use_container_width=True)
