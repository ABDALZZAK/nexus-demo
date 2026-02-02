def generate_risk_explanation(selected_date, states_trend, hotspots, alerts):
    lines = []
    lines.append(f"📅 **Date:** {selected_date}")

    if states_trend is not None and not states_trend.empty:
        top = states_trend.sort_values("mean_risk", ascending=False).head(3)
        names = ", ".join(top["NAME_1"].tolist())
        avg_top = float(top["mean_risk"].mean())
        lines.append(f"🏛️ **Top risk states:** {names} (avg ≈ {avg_top:.2f}).")

        inc = states_trend[states_trend["trend"].str.contains("↑", na=False)]
        if not inc.empty:
            inc_names = ", ".join(inc.sort_values("delta", ascending=False).head(4)["NAME_1"].tolist())
            lines.append(f"📈 **Increasing trend** in: {inc_names}.")

        dec = states_trend[states_trend["trend"].str.contains("↓", na=False)]
        if not dec.empty:
            dec_names = ", ".join(dec.sort_values("delta").head(4)["NAME_1"].tolist())
            lines.append(f"📉 **Decreasing trend** in: {dec_names}.")

        overall = float(states_trend["mean_risk"].mean())
        if overall > 0.7:
            level = "🔴 very high"
        elif overall > 0.5:
            level = "🟠 elevated"
        elif overall > 0.3:
            level = "🟡 moderate"
        else:
            level = "🟢 low"
        lines.append(f"📊 **Overall risk across Germany:** {level} (mean ≈ {overall:.2f}).")

    if hotspots is not None and not hotspots.empty:
        lines.append(f"🔥 **Hotspots:** {hotspots['cluster'].nunique()} clusters detected (score threshold).")
    else:
        lines.append("✅ **Hotspots:** none detected for this date.")

    if alerts:
        lines.append("🚨 **Alerts:**")
        for a in alerts[:6]:
            lines.append(f"- {a}")

    return "\n\n".join(lines)
