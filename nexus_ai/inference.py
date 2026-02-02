import os
import math
import joblib
import numpy as np

from nexus_ai.utils import clamp, score_to_level, level_to_recommendation, RiskResult

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "nexus_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

_model = joblib.load(MODEL_PATH)
_feature_columns = joblib.load(FEATURES_PATH)


def _build_model_features(ui: dict) -> dict:
    f = dict(ui)

    # precipitation naming
    if "precipitation" in f and "tp_mm" not in f:
        f["tp_mm"] = f["precipitation"]

    # cyclical month encoding
    if "month" in f:
        m = max(1.0, min(12.0, float(f["month"])))
        angle = 2 * math.pi * (m / 12.0)
        f["month_sin"] = math.sin(angle)
        f["month_cos"] = math.cos(angle)

    return f


def predict_risk(features: dict) -> RiskResult:
    model_features = _build_model_features(features)

    X = []
    for col in _feature_columns:
        if col not in model_features:
            raise KeyError(f"Missing feature: {col}")
        X.append(model_features[col])

    X = np.array(X, dtype=float).reshape(1, -1)

    raw_score = float(_model.predict(X)[0])
    risk_score = clamp(raw_score, 0.0, 1.0)

    risk_level = score_to_level(risk_score)
    recommendation = level_to_recommendation(risk_level)

    explanation_parts = []
    if features.get("wind_speed", 0) > 10:
        explanation_parts.append("strong winds")
    if features.get("humidity", 100) < 30:
        explanation_parts.append("low humidity")
    if features.get("temperature", 0) > 28:
        explanation_parts.append("high temperature")
    if features.get("precipitation", 0) < 1:
        explanation_parts.append("dry conditions")

    explanation = " and ".join(explanation_parts) if explanation_parts else "moderate conditions"

    return RiskResult(
        risk_score=round(risk_score, 3),
        risk_level=risk_level,
        explanation=explanation,
        recommendation=recommendation
    )
