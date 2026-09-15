# ReadyLine — Mission Readiness & Predictive Maintenance Copilot

## Team
- **Team name:** Pharmatrix
- **Track:** AI
- **Lead:** Tvisha Shah (24bph100@charusat.edu.in)
- **Members:** Patel Vaidehi Amishkumar (24bph077@charusat.edu.in), Patel Shiyaben Nimeshbhai (24bph072@charusat.edu.in), Shah Kripi Nikhil (24bph100@charusat.edu.in)

## Problem Statement
Military organisations cannot reliably determine whether aircraft, vehicles, and equipment
are mission-ready. Maintenance runs on fixed calendar schedules regardless of actual
component condition, while HUMS sensor data that could predict failures weeks in advance
sits unanalysed. Unexpected platform failures drop operational readiness and cost weeks of
recovery time.

## Solution
ReadyLine ingests HUMS sensor readings and service records for a fleet of assets, then:
1. Scores every asset's mission readiness (Ready / At Risk / Not Ready)
2. Explains *why* — which component, which sensor, how far past safe threshold
3. Predicts which components will fail before the next mission window, using trend
   extrapolation on the sensor history
4. Generates a prioritised, fleet-wide maintenance plan for crews and commanders

## Key Features
- Fleet-wide readiness dashboard
- Per-component root-cause explanations (no black box)
- Trend-based failure prediction with estimated days-to-failure
- Auto-generated prioritised maintenance plan
- Interactive Streamlit UI for live demo

## Tech Stack
- Python, Streamlit (UI), pandas / numpy (data + trend analysis)
- IBM Bob — used throughout for architecture planning, code scaffolding, and review
  (see `docs/architecture.md` for exactly where)

## How to Run
See [`docs/setup-guide.md`](docs/setup-guide.md) for full instructions. Quick version:
```bash
cd src
pip install -r requirements.txt
python data_generator.py      # creates sample fleet data
streamlit run app.py
```

## Demo
- Video: see `demo/demo-video-link.txt`
- Live demo: see `demo/live-demo-url.txt`
- Screenshots: `demo/screenshots/`

## Known Limitations
- [Fill in honestly once you've built and tested — e.g. "failure prediction uses linear
  trend extrapolation, not a trained ML model, due to hackathon time constraints"]
- [ ]

## What We're Most Proud Of
- [Fill in before submitting]
