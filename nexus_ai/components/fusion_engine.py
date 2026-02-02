def compute_fusion_score(climate_score: float, sensor_score: float | None):
    """
    Combine climate (ERA5) risk with sensor-based risk into one final score
    """
    if sensor_score is None:
        return climate_score

    climate_score = float(climate_score)
    sensor_score = float(sensor_score)

    fusion = 0.6 * climate_score + 0.4 * sensor_score
    return round(min(fusion, 1.0), 2)


def fusion_level(score: float):
    if score < 0.3:
        return "Low"
    elif score < 0.55:
        return "Moderate"
    elif score < 0.75:
        return "High"
    else:
        return "Critical"
