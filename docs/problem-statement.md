# Problem Statement

## Who is affected
Maintenance officers, fleet readiness managers, and unit commanders in military
organisations responsible for keeping aircraft, ground vehicles, and equipment
mission-ready. Also relevant to any operator of expensive, sensor-instrumented assets
(commercial aviation, heavy industrial fleets) with the same calendar-maintenance problem.

## The problem
Most maintenance programs today are **calendar-based**: a component is serviced every
N days or N flight hours, regardless of its actual measured condition. This causes two
opposite failure modes:
- **Under-maintenance**: a component degrades faster than expected (due to usage
  intensity, environment, wear) and fails between scheduled services — grounding the
  asset unexpectedly, right when it's needed for a mission.
- **Over-maintenance**: a healthy component is serviced anyway because the calendar
  says so, wasting technician time, parts, and asset downtime that could have been
  avoided.

Meanwhile, HUMS (Health & Usage Monitoring System) sensors already stream continuous
data — temperature, vibration, pressure, hours-since-service — that contains early
warning signs of failure. That data is collected but rarely analysed systematically
across a whole fleet in near-real-time, so the early warning it contains goes unused.

## Why existing solutions don't solve it
- Calendar-based maintenance software tracks *schedules*, not *condition* — it has no
  concept of "this specific engine is degrading faster than normal."
- Raw HUMS dashboards show sensor values but don't translate them into a readiness
  decision ("is this asset safe to send on the next mission?") or a prioritised action
  ("fix this component first, here's why").
- Where predictive tools exist, they are usually single-asset, single-vendor point
  solutions that don't give a fleet-wide, cross-asset prioritised view for a commander
  or maintenance planner making resource allocation decisions.

## Quantified pain
- The US military alone spends **$90B/year** on maintenance; industry analyses suggest
  a meaningful share of that is avoidable through condition-based rather than
  calendar-based maintenance.
- Every unplanned platform failure removes an asset from the mission-ready pool and can
  take **weeks** to recover from, directly reducing operational readiness at the moment
  it's needed most.

## Why this matters now
Sensor instrumentation (HUMS) is already deployed across modern military and industrial
fleets — the data exists. What's missing is the layer that turns raw sensor streams into
an explainable, prioritised, fleet-wide readiness and maintenance decision. That is
exactly the gap ReadyLine closes.
