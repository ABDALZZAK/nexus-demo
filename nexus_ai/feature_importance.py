import os
import joblib
import numpy as np
import pandas as pd
def get_model_name():
    model = joblib.load(MODEL_PATH)
    return model.__class__.__name__

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "nexus_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")


def get_feature_importance():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    # -------------------------------
    # Case 1: Tree-based models
    # -------------------------------
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_

    # -------------------------------
    # Case 2: Linear models
    # -------------------------------
    elif hasattr(model, "coef_"):
        coef = model.coef_
        # in case of multi-output
        if coef.ndim > 1:
            coef = coef[0]
        importances = np.abs(coef)

        # normalize to sum = 1
        importances = importances / np.sum(importances)

    else:
        raise ValueError(
            "Model does not support feature importance or coefficients."
        )

    df = pd.DataFrame({
        "feature": features,
        "importance": importances
    })

    df = df.sort_values("importance", ascending=False)
    df["importance_pct"] = (df["importance"] * 100).round(1)

    return df
def get_model_metrics():
    metrics_path = MODEL_PATH.replace("nexus_model.pkl", "model_metrics.pkl")

    if not os.path.exists(metrics_path):
        raise FileNotFoundError(f"Model metrics not found: {metrics_path}")

    return joblib.load(metrics_path)
