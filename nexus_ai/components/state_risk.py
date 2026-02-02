import streamlit as st
import geopandas as gpd
import pydeck as pdk

DARK_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"


@st.cache_data(show_spinner=False)
def load_states(states_path):
    gdf = gpd.read_file(states_path)

    candidates = [
        "NAME_1", "name", "NAME", "state", "STATE",
        "VARNAME_1", "NL_NAME_1", "NAME_EN"
    ]

    found = None
    for c in candidates:
        if c in gdf.columns:
            found = c
            break

    if found is None:
        raise ValueError(
            f"State name column not found. Available columns: {list(gdf.columns)}"
        )

    if found != "NAME_1":
        gdf = gdf.rename(columns={found: "NAME_1"})

    # Ensure CRS is WGS84
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    else:
        gdf = gdf.to_crs("EPSG:4326")

    return gdf


def compute_state_risk(df, states_gdf):
    lat_col = next((c for c in df.columns if c.lower() in ["lat", "latitude"]), None)
    lon_col = next((c for c in df.columns if c.lower() in ["lon", "long", "longitude"]), None)

    if lat_col is None or lon_col is None:
        raise ValueError("Latitude/Longitude columns not found in df.")
    if "risk_score" not in df.columns:
        raise ValueError("Column 'risk_score' not found in df.")

    gdf_pts = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )

    joined = gpd.sjoin(
        gdf_pts,
        states_gdf[["NAME_1", "geometry"]],
        how="inner",
        predicate="within"
    )

    agg = (
        joined
        .groupby("NAME_1")
        .agg(
            mean_risk=("risk_score", "mean"),
            max_risk=("risk_score", "max"),
            cells=("risk_score", "count"),
        )
        .reset_index()
    )

    out = states_gdf.merge(agg, on="NAME_1", how="left")
    out["mean_risk"] = out["mean_risk"].fillna(0.0)
    out["max_risk"] = out["max_risk"].fillna(0.0)
    out["cells"] = out["cells"].fillna(0).astype(int)

    return out


def render_state_risk_map(states_gdf):
    if states_gdf.empty:
        st.warning("No state data to render.")
        return

    layer = pdk.Layer(
        "GeoJsonLayer",
        states_gdf,
        pickable=True,
        opacity=0.55,
        stroked=True,
        filled=True,
        get_line_color=[220, 220, 220],
        get_line_width=80,
        get_fill_color="[255 * mean_risk, 60, 255 * (1 - mean_risk)]",
    )

    view = pdk.ViewState(latitude=51.0, longitude=10.0, zoom=5.3)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style=DARK_STYLE,
        tooltip={
            "html": """
            <b>{NAME_1}</b><br/>
            Mean risk: {mean_risk}<br/>
            Max risk: {max_risk}<br/>
            Cells: {cells}
            """,
            "style": {"backgroundColor": "#111", "color": "white"},
        },
    )

    st.pydeck_chart(deck, use_container_width=True)
