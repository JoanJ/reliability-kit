# SLI / SLO worksheet — {{company}}

One row per critical user journey. Start with `{{services}}` — add more only
after the first set has been running for a quarter.

## The worksheet

| Service | SLI (what we measure) | Data source | SLO | Window | Owner |
|---|---|---|---|---|---|
| {{services}} | _e.g. successful requests / total_ | {{stack.metrics}} | _e.g. 99.9%_ | 30d | _name_ |
| | | | | | |
| | | | | | |

## Rules for picking SLIs

1. **Measure what the user feels**, not what the machine does. "CPU 70%" is
   not an SLI; "checkout succeeded" is
2. **Prefer ratios over averages** — a 99.9% success rate with a 5-minute
   total outage looks different from constant 300ms latency
3. **Use data you already collect.** If it needs a new pipeline, it will not
   ship this quarter
4. **Two or three SLIs per service**, no more — the rest are diagnostics

## Choosing the number

| SLO | Meaning | Use when |
|---|---|---|
| 99.9% | ~43 min downtime / month | Internal tools, low blast radius |
| 99.95% | ~22 min / month | Typical customer-facing API |
| 99.99% | ~4 min / month | Revenue-critical, high load — costs real money |

Start slightly **below** what you already achieve, so the error budget is
honest and the team isn't in permanent deficit on day one.

## Review agenda (30 min, monthly)

1. Error budget remaining — burn rate trend
2. Any SLO breach: what happened, what changed
3. Proposed changes: tighten, loosen, or add a service
4. Action items → `30-incidents/action-tracker.csv`

## Anti-patterns

- SLO on infrastructure nobody can name the user of
- 100% SLOs (no budget = no signal)
- Setting SLOs from a vendor benchmark instead of your own telemetry
- Never revisiting the number — review it monthly or it's fiction
