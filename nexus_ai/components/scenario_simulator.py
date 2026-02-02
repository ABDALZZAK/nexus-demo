import streamlit as st
import numpy as np


def render_scenario_simulator():
    """
    What-if Scenario Simulator
    Allows the user to modify climate parameters and observe
    the hypothetical impact on wildfire risk.
    """

    st.markdown("### 🔮 Scenario Parameters")
    st.caption(
        "Simulate hypothetical climate conditions and evaluate "
        "their impact on wildfire risk."
    )

    # --------------------------------------------------
    # Scenario inputs
    # --------------------------------------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        delta_temp = st.slider(
            "Δ Temperature (°C)",
            min_value=-10,
            max_value=10,
            value=0,
            step=1
        )

    with c2:
        delta_hum = st.slider(
            "Δ Humidity (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=5
        )

    with c3:
        delta_wind = st.slider(
            "Δ Wind Speed (km/h)",
            min_value=-20,
            max_value=20,
            value=0,
            step=2
        )

    st.divider()

    # --------------------------------------------------
    # Baseline reference
    # --------------------------------------------------
    base_risk = st.session_state.get("baseline_risk_score", None)

    if base_risk is None:
        st.info(
            "ℹ️ No baseline risk found.\n\n"
            "Run the main AI analysis first to establish a reference."
        )
        base_risk = 0.5  # safe neutral fallback

    # --------------------------------------------------
    # Simple explainable scenario model
    # --------------------------------------------------
    scenario_risk = (
        base_risk
        + 0.015 * delta_temp
        - 0.010 * delta_hum
        + 0.020 * delta_wind
    )

    scenario_risk = float(np.clip(scenario_risk, 0.0, 1.0))

    # --------------------------------------------------
    # Execute scenario
    # --------------------------------------------------
    if st.button("🧪 Run Scenario Simulation", use_container_width=True):
        st.session_state["scenario_risk_score"] = scenario_risk

        st.success("Scenario executed successfully ✔️")

    # --------------------------------------------------
    # Output summary
    # --------------------------------------------------
    st.markdown("### 📊 Scenario Result")

    st.metric(
        label="Scenario Risk Score",
        value=round(scenario_risk, 2),
        delta=round(scenario_risk - base_risk, 2)
    )

    st.caption(
        "Positive delta indicates increased wildfire risk under "
        "the simulated conditions."
    )

    st.markdown(
        """
**Interpretation logic**
- Higher temperature → increases ignition probability  
- Lower humidity → dries fuels  
- Stronger wind → accelerates spread  

This scenario engine is intentionally **transparent and explainable**.
"""
    )
