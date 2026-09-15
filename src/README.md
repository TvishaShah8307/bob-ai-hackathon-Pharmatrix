# src/ layout

- `data_generator.py` — generates synthetic fleet data (assets, sensor readings,
  service records) into `data/`. Run this once before starting the app.
- `predictor.py` — core logic: readiness scoring, trend-based failure prediction,
  explanation generation, and fleet-wide maintenance plan ranking. No UI code here —
  keep this module UI-agnostic so it's testable and reusable.
- `app.py` — Streamlit dashboard. Imports `predictor.py`, loads `data/*.csv`, and
  renders the fleet view, asset drill-down, and maintenance plan.
- `data/` — generated CSVs (`assets.csv`, `sensor_readings.csv`,
  `service_records.csv`). Not meant to be hand-edited; regenerate with
  `python data_generator.py`.
- `.env.example` — template for any config/secrets if you extend the app beyond local
  CSV data.

Run order: `pip install -r requirements.txt` → `python data_generator.py` →
`streamlit run app.py`.
