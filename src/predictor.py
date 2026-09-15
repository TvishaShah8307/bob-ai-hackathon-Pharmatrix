"""
predictor.py
Core, UI-agnostic logic for ReadyLine:
  - per-component risk scoring (sensor deviation + calendar overdue)
  - per-asset readiness rollup (Ready / At Risk / Not Ready)
  - trend-based failure prediction (linear extrapolation)
  - plain-language explanations
  - fleet-wide prioritised maintenance plan

No Streamlit/UI imports here on purpose, so this module can be tested and reused
independently of the dashboard.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

TODAY = datetime(2026, 9, 15)

READY_THRESHOLD = 18     # risk_score below this => Ready
AT_RISK_THRESHOLD = 45   # risk_score below this => At Risk, else Not Ready


def component_risk_score(latest_value: float, threshold: float, days_overdue: int) -> float:
    """
    Combine sensor deviation (% over threshold) and calendar overdue days into a
    single 0-100+ risk score. Transparent and explainable by design.
    """
    deviation_pct = max(0.0, (latest_value - threshold) / threshold) * 100
    overdue_penalty = max(0, days_overdue) * 0.6  # 0.6 points per day overdue
    score = deviation_pct * 2.2 + overdue_penalty
    return round(min(score, 150), 1)


def readiness_status(risk_score: float) -> str:
    if risk_score < READY_THRESHOLD:
        return "Ready"
    if risk_score < AT_RISK_THRESHOLD:
        return "At Risk"
    return "Not Ready"


def predict_days_to_failure(history: pd.DataFrame, threshold: float):
    """
    Fit a simple linear trend to a component's recent sensor history and estimate
    the number of days until the value crosses its failure threshold.
    Returns None if the trend is flat/decreasing (no predicted failure) or if
    there isn't enough history.
    """
    if len(history) < 5:
        return None

    history = history.sort_values("timestamp")
    x = np.arange(len(history))
    y = history["value"].values

    slope, intercept = np.polyfit(x, y, 1)
    if slope <= 0:
        return None  # not trending toward failure

    latest_value = y[-1]
    if latest_value >= threshold:
        return 0  # already past threshold

    days_to_cross = (threshold - latest_value) / slope
    return int(round(days_to_cross)) if days_to_cross < 365 else None


def explain(component: str, latest_value: float, threshold: float, unit: str,
            days_overdue: int, days_to_failure) -> str:
    reasons = []
    if latest_value > threshold:
        pct = round((latest_value - threshold) / threshold * 100, 1)
        reasons.append(
            f"{component} reading is {latest_value}{unit} vs safe threshold {threshold}{unit} "
            f"({pct}% over)."
        )
    if days_overdue > 0:
        reasons.append(f"{component} service is {days_overdue} days overdue.")
    if days_to_failure is not None and days_to_failure > 0:
        reasons.append(f"Trend suggests threshold breach in ~{days_to_failure} days if unaddressed.")
    if not reasons:
        return f"{component} is within normal operating range."
    return " ".join(reasons)


def score_fleet(assets_df: pd.DataFrame, sensors_df: pd.DataFrame,
                 service_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a per-(asset, component) DataFrame with risk score, status, explanation,
    and predicted days-to-failure — the core scored dataset the whole app is built on.
    """
    rows = []
    sensors_df = sensors_df.copy()
    sensors_df["timestamp"] = pd.to_datetime(sensors_df["timestamp"])
    service_df = service_df.copy()
    service_df["last_service_date"] = pd.to_datetime(service_df["last_service_date"])

    for _, asset in assets_df.iterrows():
        asset_id = asset["asset_id"]
        comp_history = sensors_df[sensors_df["asset_id"] == asset_id]

        for component in comp_history["component"].unique():
            hist = comp_history[comp_history["component"] == component].sort_values("timestamp")
            latest = hist.iloc[-1]
            threshold = float(latest["threshold"])
            unit = latest["unit"]

            svc = service_df[(service_df["asset_id"] == asset_id) & (service_df["component"] == component)]
            if len(svc):
                svc_row = svc.iloc[0]
                days_since_service = (TODAY - svc_row["last_service_date"]).days
                days_overdue = max(0, days_since_service - int(svc_row["service_interval_days"]))
            else:
                days_overdue = 0

            days_to_failure = predict_days_to_failure(hist, threshold)
            risk = component_risk_score(float(latest["value"]), threshold, days_overdue)
            status = readiness_status(risk)
            reason = explain(component, float(latest["value"]), threshold, unit, days_overdue, days_to_failure)

            rows.append({
                "asset_id": asset_id,
                "asset_type": asset["asset_type"],
                "fleet": asset["fleet"],
                "component": component,
                "latest_value": latest["value"],
                "threshold": threshold,
                "unit": unit,
                "days_overdue": days_overdue,
                "risk_score": risk,
                "status": status,
                "days_to_failure": days_to_failure,
                "explanation": reason,
            })

    return pd.DataFrame(rows)


def asset_readiness(scored_df: pd.DataFrame) -> pd.DataFrame:
    """Roll component-level scores up to one row per asset (worst-case component wins)."""
    agg = (
        scored_df.groupby(["asset_id", "asset_type", "fleet"])
        .agg(risk_score=("risk_score", "max"), flagged_components=("status", lambda s: (s != "Ready").sum()))
        .reset_index()
    )
    agg["status"] = agg["risk_score"].apply(readiness_status)
    return agg.sort_values("risk_score", ascending=False)


def maintenance_plan(scored_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Fleet-wide prioritised list of every flagged (non-Ready) component."""
    flagged = scored_df[scored_df["status"] != "Ready"].copy()
    flagged = flagged.sort_values(
        by=["risk_score", "days_to_failure"],
        ascending=[False, True],
        na_position="last",
    )
    flagged["priority"] = range(1, len(flagged) + 1)
    cols = ["priority", "asset_id", "fleet", "component", "status", "risk_score",
            "days_to_failure", "explanation"]
    return flagged[cols].head(top_n)
