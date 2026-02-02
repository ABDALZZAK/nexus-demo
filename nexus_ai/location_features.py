import pandas as pd
import numpy as np

_DF = None

def load_daily_risk(path="daily_risk.parquet"):
    global _DF
    if _DF is None:
        _DF = pd.read_parquet(path)
    return _DF


def get_risk_from_location(lat, lon, month=None):
    """
    Returns nearest AI-computed risk from daily_risk.parquet
    """

    df = load_daily_risk()

    # optional month filter
    if month is not None and "month" in df.columns:
        df = df[df["month"] == month]

    # nearest grid point
    dist = (df["latitude"] - lat) ** 2 + (df["longitude"] - lon) ** 2
    row = df.loc[dist.idxmin()]

    return {
        "risk_score": float(row["risk_score"]),
        "risk_level": row["risk_level"],
    }
