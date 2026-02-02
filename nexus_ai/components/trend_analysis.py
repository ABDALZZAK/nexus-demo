import pandas as pd
from typing import Optional


def compute_state_trend(
    today_states: pd.DataFrame,
    yesterday_states: Optional[pd.DataFrame]
) -> pd.DataFrame:
    """
    Compute per-state wildfire risk trend between today and yesterday.

    Returns:
    - delta: numeric difference in mean risk
    - trend: categorical label (increasing / decreasing / stable / new)
    """

    # Defensive copy
    today = today_states.copy()

    # If no yesterday data → mark as new
    if yesterday_states is None or yesterday_states.empty:
        today["mean_risk_yesterday"] = 0.0
        today["delta"] = 0.0
        today["trend"] = "new"
        return today

    # Ensure required columns exist
    required_cols = {"NAME_1", "mean_risk"}
    if not required_cols.issubset(today.columns):
        raise ValueError(f"today_states must contain {required_cols}")
    if not required_cols.issubset(yesterday_states.columns):
        raise ValueError(f"yesterday_states must contain {required_cols}")

    yesterday = yesterday_states[["NAME_1", "mean_risk"]].copy()
    yesterday = yesterday.rename(columns={"mean_risk": "mean_risk_yesterday"})

    merged = today.merge(
        yesterday,
        on="NAME_1",
        how="left"
    )

    merged["mean_risk_yesterday"] = merged["mean_risk_yesterday"].fillna(0.0)

    # Numeric delta
    merged["delta"] = merged["mean_risk"] - merged["mean_risk_yesterday"]

    # Trend classification
    def label_trend(d: float) -> str:
        if d > 0.05:
            return "increasing"
        if d < -0.05:
            return "decreasing"
        return "stable"

    merged["trend"] = merged["delta"].apply(label_trend)

    return merged
