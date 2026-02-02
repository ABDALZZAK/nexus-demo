def generate_alerts(states_risk, hotspots):
    alerts = []

    if states_risk is not None and not states_risk.empty:
        high_states = states_risk[states_risk["mean_risk"] > 0.7]["NAME_1"].tolist()
        for s in high_states[:6]:
            alerts.append(f"🔴 High wildfire risk in **{s}** (mean_risk > 0.7).")

    if hotspots is not None and not hotspots.empty:
        alerts.append(f"🔥 **{hotspots['cluster'].nunique()} hotspots** detected (high-risk clusters).")

    if not alerts:
        alerts.append("✅ No critical alerts for the selected date based on current thresholds.")

    return alerts
