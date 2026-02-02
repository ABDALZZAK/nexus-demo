from __future__ import annotations
from typing import Dict, List, Tuple

def explain_stub(features: Dict) -> List[Tuple[str, float]]:
    """
    يرجع أهمية عوامل بشكل مبسط لواجهة MVP.
    لاحقًا نستبدله بـ feature importance حقيقي من موديل الكولاب (RF/SHAP).
    """
    temperature = float(features["temperature"])
    wind_speed = float(features["wind_speed"])
    humidity = float(features["humidity"])
    precipitation = float(features["precipitation"])

    # heuristic weights (0..1)
    w_wind = min(wind_speed / 20, 1.0)
    w_hum = min((100 - humidity) / 100, 1.0)
    w_temp = min((temperature - 5) / 40, 1.0)
    w_rain = min((10 - precipitation) / 10, 1.0)

    total = w_wind + w_hum + w_temp + w_rain
    if total <= 0:
        return [("wind_speed", 0.25), ("humidity", 0.25), ("temperature", 0.25), ("precipitation", 0.25)]

    return [
        ("wind_speed", w_wind / total),
        ("humidity", w_hum / total),
        ("temperature", w_temp / total),
        ("precipitation", w_rain / total),
    ]
