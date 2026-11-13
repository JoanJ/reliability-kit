# Metric definitions — formulas, not vibes

Every number in the monthly report is defined here. If a definition changes,
the history changes with it — note it in the changelog at the bottom.

## Golden signals (per service)

| Signal | Definition | Notes |
|---|---|---|
| **Latency** | p95/p99 of request duration | Percentiles only — never the mean |
| **Traffic** | requests/second (or jobs/second for workers) | Demand, not health |
| **Errors** | failed requests / total requests | Match your SLI definition exactly |
| **Saturation** | how full the resource is (queue depth, CPU, connections) | The leading indicator — it predicts the outage |

## RED — per service (request-driven)

```
Rate:      request rate per service
Errors:    error rate = 5xx / total  (or your SLI's failure definition)
Duration:  latency percentiles (p50, p95, p99)
```
Applies to each of: `{{services}}`

## USE — per resource (infra, pools, data stores)

```
Utilization:  % of capacity in use over a window (CPU, memory, disk, IOPS)
Saturation:   queue depth, pending work, connection pool wait
Errors:       hardware/software errors (retryable vs not)
```
Apply to every host, container, DB, cache, queue, load balancer, third-party
quota.

## DORA — the four, reported quarterly

| Metric | Definition | How to get it |
|---|---|---|
| **Lead time for change** | commit → running in production (median) | VCS + deploy events |
| **Deploy frequency** | production deploys per day per service | deploy events |
| **Change failure rate** | % of deploys causing rollback/hotfix/incident | deploys × incident links |
| **MTTR** | time from incident declare → user impact ends (sev-1/2) | `30-incidents/` timeline |

## SLO / error budget

```
SLI       = numerator / denominator of the thing users feel
SLO       = target over a window (e.g. 99.9% / 30d)
Budget    = 1 − SLO over the window
Burn rate = budget consumed per unit time (1.0 = whole budget in the window)
```

Multi-window burn alerts (page on the fast one):

```
fast:  2% of 30d budget in 1h   AND  2% in 5m
slow:  5% of 30d budget in 6h   AND  1% in 30m
```
Policy: `10-slos/error-budget-policy.md`.

## Incident metrics

| Metric | Definition |
|---|---|
| **MTTD** | first signal → incident declared |
| **MTTA** | declared → first responder acknowledged |
| **MTTR** | declared → user impact ends (not "incident closed") |
| **Detect ratio** | % of incidents found by alert vs by customer |
| **Action closure** | % of postmortem actions closed ≤30 days |

## Human metrics (the ones managers forget)

| Metric | Definition | Source |
|---|---|---|
| **Pages/SRE/week** | total pages ÷ on-call headcount | {{stack.paging}} |
| **Toil hours/week** | time on repetitive, automatable work | alert audit + timesheet estimate |
| **After-hours pages** | pages outside {{engineering_hours}} | {{stack.paging}} |

## Business signals (tie reliability to money)

Track at least one per journey: `{{services}}` — e.g. checkout success rate,
login success rate, search zero-result rate. When an SLO burns, this is the
number that says what it cost.

## Changelog

| Date | Definition changed | Why |
|---|---|---|
| | | |
