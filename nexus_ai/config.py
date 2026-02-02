from dataclasses import dataclass

@dataclass(frozen=True)
class RiskThresholds:
    low: float = 0.30
    medium: float = 0.60
    high: float = 0.80

THRESHOLDS = RiskThresholds()
FEATURES = ["temperature", "wind_speed", "humidity", "precipitation", "month"]
