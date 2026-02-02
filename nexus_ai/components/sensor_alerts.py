import pandas as pd


def generate_sensor_alerts(df_sensors: pd.DataFrame):
    """
    Generates human-readable alerts based on Birdhouse sensor signals.
    This layer acts as a local confirmation / escalation logic.
    """

    alerts = []

    if df_sensors is None or df_sensors.empty:
        return alerts

    # Ensure numeric
    for c in ["pm25", "temp_c", "rh"]:
        if c in df_sensors.columns:
            df_sensors[c] = pd.to_numeric(df_sensors[c], errors="coerce")

    # Use latest reading per device
    if "timestamp_utc" in df_sensors.columns:
        df_latest = (
            df_sensors
            .sort_values("timestamp_utc")
            .groupby("device_id", as_index=False)
            .tail(1)
        )
    else:
        df_latest = df_sensors.copy()

    # --------------------------------------------------
    # Rule-based alerts (explainable & operational)
    # --------------------------------------------------
    for _, row in df_latest.iterrows():
        device = row.get("device_id", "Unknown")

        pm25 = row.get("pm25", 0)
        temp = row.get("temp_c", 0)
        rh = row.get("rh", 100)

        # 🔥 Smoke escalation
        if pm25 >= 150:
            alerts.append(
                f"🔥 Birdhouse {device}: extreme smoke concentration detected (PM2.5={pm25:.0f})"
            )
        elif pm25 >= 80:
            alerts.append(
                f"⚠️ Birdhouse {device}: elevated smoke levels (PM2.5={pm25:.0f})"
            )

        # 🌡️ Heat anomaly
        if temp >= 45:
            alerts.append(
                f"🌡️ Birdhouse {device}: abnormal temperature spike ({temp:.1f}°C)"
            )

        # 💧 Dry conditions
        if rh <= 20:
            alerts.append(
                f"💧 Birdhouse {device}: critically low humidity ({rh:.0f}%)"
            )

        # 🔥 Combined confirmation
        if pm25 >= 80 and temp >= 35 and rh <= 30:
            alerts.append(
                f"🚨 Birdhouse {device}: MULTI-SENSOR FIRE CONFIRMATION"
            )

    return alerts
