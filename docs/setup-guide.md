# Setup Guide

Follow these steps exactly on a clean machine / fresh terminal — this is what judges
will do to verify the project runs.

## Prerequisites
- Python 3.9 or later
- `pip`
- No accounts, API keys, or external services are required — the hackathon build runs
  entirely on local synthetic data.

## Environment variables
None are required to run the demo. `src/.env.example` lists optional variables only
needed if you extend the app to a real data source (see comments in that file).

## Install
```bash
cd src
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Generate sample data
```bash
python data_generator.py
```
This creates `src/data/assets.csv`, `src/data/sensor_readings.csv`, and
`src/data/service_records.csv` — a synthetic fleet of 15 assets with realistic HUMS
sensor histories (some intentionally degrading, to demonstrate the prediction feature).

## Run
```bash
streamlit run app.py
```
Streamlit will print a local URL (typically `http://localhost:8501`) — open it in a
browser.

## How to verify it's working
1. The Fleet Readiness table loads with 15 assets, each showing a Ready / At Risk /
   Not Ready status.
2. Selecting an asset in "Asset Detail" shows its components; expanding a flagged
   component shows a plain-language explanation and a sensor trend chart.
3. The "Prioritised Maintenance Plan" table at the bottom lists every flagged
   component fleet-wide, ranked by priority, and can be downloaded as CSV.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` inside `src/` (and make sure your virtualenv is activated) |
| App loads but shows "No data found" | Run `python data_generator.py` from inside `src/` first, then rerun `streamlit run app.py` |
| `streamlit: command not found` | Use `python -m streamlit run app.py` instead, or ensure the venv's `bin`/`Scripts` folder is on your PATH |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| Charts look empty for an asset | That asset/component may have a flat (non-degrading) trend by design — try a different asset from the Fleet Readiness table with an "At Risk" or "Not Ready" status |
