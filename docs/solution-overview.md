# Solution Overview

## Core mechanism
ReadyLine turns three raw inputs — asset metadata, HUMS sensor readings, and service
records — into a fleet-wide readiness and maintenance decision, in three stages:

1. **Readiness scoring (per component → per asset)**
   For every component on every asset, the most recent sensor reading is compared
   against its safe operating threshold. A component's deviation (how far past
   threshold, as a percentage) plus its "days overdue" against its service interval
   are combined into a component risk score. An asset's overall readiness score is the
   worst-case combination of its components' risk scores, classified as
   **Ready / At Risk / Not Ready**.

2. **Explanation**
   Every readiness score is paired with a plain-language explanation: which component,
   which sensor, its current value vs. threshold, and whether it's a sensor-condition
   issue, a calendar-overdue issue, or both. Nothing is a black-box number — a
   maintenance officer can see exactly why an asset is flagged.

3. **Trend-based failure prediction**
   For components with enough sensor history, ReadyLine fits a simple linear trend to
   recent readings and extrapolates forward to estimate the date the value will cross
   its failure threshold — giving an estimated "days to failure" instead of just a
   current snapshot. This is the piece that lets maintenance be *predictive* rather than
   reactive.

4. **Prioritised maintenance plan**
   All flagged components across the entire fleet are ranked by a combination of risk
   score and estimated days-to-failure, producing a single prioritised action list —
   telling commanders and crews what to fix first, fleet-wide, not just asset-by-asset.

## What makes it different from naive alternatives
- A naive dashboard just plots sensor values — it doesn't turn them into a readiness
  decision or a ranked action list.
- A naive "red/yellow/green" status ignores *why* an asset is flagged — ReadyLine always
  attaches the component-level explanation.
- ReadyLine is explicitly **fleet-wide and prioritised**, not single-asset — the
  maintenance plan output is the thing a resource-constrained maintenance crew actually
  needs: "given limited technician hours, work this list in this order."

## Key design decisions
- **Explainability over black-box ML**: readiness scoring and failure prediction use
  transparent, auditable logic (threshold deviation, linear trend extrapolation) rather
  than an opaque trained model — important in a domain where maintenance crews must
  trust and act on the output under time pressure.
- **Fleet-first UX**: the primary view is always the whole fleet ranked by risk, with
  drill-down into a single asset — not the other way around — because the commander's
  question is "what needs attention across everything I have," not "how is this one
  asset doing."
- **Synthetic but realistic data**: for the hackathon, sensor and service data is
  generated to mimic real HUMS patterns (including deliberately-degrading components),
  since real defence sensor data isn't available — the analysis pipeline itself is built
  to run unchanged against real HUMS exports.

## User experience
A maintenance planner opens the ReadyLine dashboard and immediately sees the fleet
sorted by readiness risk. Clicking into a flagged asset shows exactly which
component(s) are driving the score, the sensor trend chart, and the predicted
days-to-failure. At the fleet level, a single "Maintenance Plan" view lists every
flagged component across every asset, ranked by priority, ready to hand to a crew.
