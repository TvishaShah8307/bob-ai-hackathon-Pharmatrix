"""
data_generator.py
Generates synthetic fleet data mimicking HUMS (Health & Usage Monitoring System)
sensor exports, for demo purposes only.

Creates, under data/:
  - assets.csv
  - sensor_readings.csv
  - service_records.csv

Run: python data_generator.py
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

ASSET_TYPES = ["Aircraft", "Ground Vehicle", "Generator Unit"]
COMPONENTS = {
    "Engine": {"sensor": "temperature_c", "threshold": 120, "unit": "°C", "service_interval_days": 90},
    "Rotor/Drivetrain": {"sensor": "vibration_mm_s", "threshold": 7.0, "unit": "mm/s", "service_interval_days": 60},
    "Hydraulics": {"sensor": "pressure_psi_dev", "threshold": 15.0, "unit": "psi deviation", "service_interval_days": 45},
    "Avionics/Electrical": {"sensor": "fault_count", "threshold": 5, "unit": "faults/day", "service_interval_days": 120},
}

N_ASSETS = 15
DAYS_HISTORY = 30
TODAY = datetime(2026, 9, 15)


def make_assets():
    rows = []
    for i in range(1, N_ASSETS + 1):
        asset_id = f"A-{i:03d}"
        asset_type = random.choice(ASSET_TYPES)
        rows.append({
            "asset_id": asset_id,
            "asset_type": asset_type,
            "fleet": "Alpha Squadron" if i <= 8 else "Bravo Squadron",
        })
    return pd.DataFrame(rows)


def make_service_records(assets_df):
    rows = []
    for _, asset in assets_df.iterrows():
        for comp_name, comp in COMPONENTS.items():
            # most components serviced somewhat recently; a few overdue on purpose
            days_since_service = random.choice(
                [random.randint(5, comp["service_interval_days"] - 10)] * 3
                + [random.randint(comp["service_interval_days"] + 5, comp["service_interval_days"] + 50)]
            )
            last_service_date = TODAY - timedelta(days=days_since_service)
            rows.append({
                "asset_id": asset["asset_id"],
                "component": comp_name,
                "last_service_date": last_service_date.strftime("%Y-%m-%d"),
                "service_interval_days": comp["service_interval_days"],
            })
    return pd.DataFrame(rows)


def make_sensor_readings(assets_df):
    rows = []
    # pick ~1/3 of asset-components to be "degrading" for a realistic mix
    for _, asset in assets_df.iterrows():
        for comp_name, comp in COMPONENTS.items():
            degrading = random.random() < 0.28
            severity = random.uniform(0.2, 0.6) if degrading else 0  # how far past threshold it ends up
            baseline = comp["threshold"] * random.uniform(0.55, 0.75)
            for d in range(DAYS_HISTORY, 0, -1):
                date = TODAY - timedelta(days=d)
                noise = np.random.normal(0, comp["threshold"] * 0.03)
                if degrading:
                    # linear drift upward toward/past threshold over the window
                    drift = (comp["threshold"] * severity) * (1 - d / DAYS_HISTORY)
                    value = baseline + drift + noise
                else:
                    value = baseline + noise
                value = max(value, 0)
                rows.append({
                    "asset_id": asset["asset_id"],
                    "component": comp_name,
                    "sensor_type": comp["sensor"],
                    "value": round(float(value), 2),
                    "threshold": comp["threshold"],
                    "unit": comp["unit"],
                    "timestamp": date.strftime("%Y-%m-%d"),
                })
    return pd.DataFrame(rows)


def main():
    assets_df = make_assets()
    service_df = make_service_records(assets_df)
    sensors_df = make_sensor_readings(assets_df)

    assets_df.to_csv(os.path.join(OUT_DIR, "assets.csv"), index=False)
    service_df.to_csv(os.path.join(OUT_DIR, "service_records.csv"), index=False)
    sensors_df.to_csv(os.path.join(OUT_DIR, "sensor_readings.csv"), index=False)

    print(f"Generated {len(assets_df)} assets, {len(service_df)} service records, "
          f"{len(sensors_df)} sensor readings into {OUT_DIR}/")


if __name__ == "__main__":
    main()
