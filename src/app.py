"""
app.py
ReadyLine — Mission Readiness & Predictive Maintenance Copilot
Streamlit dashboard.

Run:
    python data_generator.py   # once, to create sample data
    streamlit run app.py
"""

import os

import pandas as pd
import streamlit as st

from predictor import score_fleet, asset_readiness, maintenance_plan

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

st.set_page_config(page_title="ReadyLine — Mission Readiness Copilot", layout="wide")


@st.cache_data
def load_data():
    assets_path = os.path.join(DATA_DIR, "assets.csv")
    sensors_path = os.path.join(DATA_DIR, "sensor_readings.csv")
    service_path = os.path.join(DATA_DIR, "service_records.csv")

    if not (os.path.exists(assets_path) and os.path.exists(sensors_path) and os.path.exists(service_path)):
        return None, None, None

    return (
        pd.read_csv(assets_path),
        pd.read_csv(sensors_path),
        pd.read_csv(service_path),
    )


assets_df, sensors_df, service_df = load_data()

st.title("🛠️ ReadyLine — Mission Readiness & Predictive Maintenance Copilot")
st.caption("Ingests HUMS sensor data + service records → explains readiness issues → "
           "predicts failures → generates a prioritised maintenance plan.")

if assets_df is None:
    st.error(
        "No data found. Run `python data_generator.py` first to create sample fleet "
        "data in `src/data/`, then reload this page."
    )
    st.stop()

scored = score_fleet(assets_df, sensors_df, service_df)
fleet_summary = asset_readiness(scored)
plan = maintenance_plan(scored)

status_colors = {"Ready": "🟢", "At Risk": "🟡", "Not Ready": "🔴"}

# --- Sidebar filters ---
st.sidebar.header("Filters")
fleets = ["All"] + sorted(fleet_summary["fleet"].unique().tolist())
selected_fleet = st.sidebar.selectbox("Fleet", fleets)

if selected_fleet != "All":
    fleet_summary_view = fleet_summary[fleet_summary["fleet"] == selected_fleet]
else:
    fleet_summary_view = fleet_summary

# --- Top-line metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Assets tracked", len(fleet_summary_view))
col2.metric("Ready", int((fleet_summary_view["status"] == "Ready").sum()))
col3.metric("At Risk", int((fleet_summary_view["status"] == "At Risk").sum()))
col4.metric("Not Ready", int((fleet_summary_view["status"] == "Not Ready").sum()))

st.divider()

# --- Fleet readiness table ---
st.subheader("Fleet Readiness")
display_df = fleet_summary_view.copy()
display_df["status"] = display_df["status"].apply(lambda s: f"{status_colors[s]} {s}")
st.dataframe(
    display_df[["asset_id", "asset_type", "fleet", "status", "risk_score", "flagged_components"]]
    .rename(columns={
        "asset_id": "Asset", "asset_type": "Type", "fleet": "Fleet",
        "status": "Status", "risk_score": "Risk Score", "flagged_components": "Flagged Components",
    }),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# --- Asset drill-down ---
st.subheader("Asset Detail")
asset_ids = fleet_summary_view["asset_id"].tolist()
selected_asset = st.selectbox("Select an asset to inspect", asset_ids)

asset_components = scored[scored["asset_id"] == selected_asset]
for _, row in asset_components.iterrows():
    icon = status_colors[row["status"]]
    with st.expander(f"{icon} {row['component']} — {row['status']} (risk {row['risk_score']})"):
        st.write(row["explanation"])
        history = sensors_df[
            (sensors_df["asset_id"] == selected_asset) & (sensors_df["component"] == row["component"])
        ].sort_values("timestamp")
        chart_df = history.set_index("timestamp")[["value"]]
        chart_df["threshold"] = row["threshold"]
        st.line_chart(chart_df)
        if row["days_to_failure"] is not None:
            st.warning(f"Predicted threshold breach in ~{row['days_to_failure']} days at current trend.")

st.divider()

# --- Maintenance plan ---
st.subheader("Prioritised Maintenance Plan (Fleet-wide)")
st.caption("Every flagged component across the fleet, ranked by risk and urgency.")
st.dataframe(
    plan.rename(columns={
        "priority": "#", "asset_id": "Asset", "fleet": "Fleet", "component": "Component",
        "status": "Status", "risk_score": "Risk Score", "days_to_failure": "Days to Failure",
        "explanation": "Why",
    }),
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download maintenance plan (CSV)",
    data=plan.to_csv(index=False),
    file_name="readyline_maintenance_plan.csv",
    mime="text/csv",
)
