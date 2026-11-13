# Coverage — what to measure, layer by layer

A metric gap is invisible until an outage. Work down this list; a layer is
"covered" when every row has an owner, a dashboard and (where marked) an alert.

Legend: **P** = pages · **N** = notifies (ticket/Slack) · **D** = dashboard only

| # | Layer | What to measure | Alert |
|---|---|---|---|
| 1 | **User journeys** | SLOs on `{{services}}` — success rate, latency p99, burn | **P** (burn) |
| 2 | **Business** | One money signal per journey (checkout/login/search success) | **D** |
| 3 | **Service (RED)** | rate, errors, latency percentiles per service | **P** on error/latency SLO |
| 4 | **Edge / CDN / LB** | 4xx/5xx ratio, origin offload, connection errors | **N** |
| 5 | **Async / queues** | consumer lag, queue depth, dead-letter rate, age of oldest message | **P** on lag, **N** on depth |
| 6 | **Data stores** | replication lag, connection saturation, slow queries, backup age | **P** on lag/saturation |
| 7 | **Infra (USE)** | CPU, memory, disk, IOPS per host/pool; cert expiry; node health | **N** (cert expiry: **P**) |
| 8 | **Dependencies / 3rd party** | upstream error rate, latency, quota remaining, deprecation notices | **P** on error, **N** on quota |
| 9 | **Delivery (DORA)** | deploy frequency, lead time, change failure rate, rollback rate | **D** |
| 10 | **Security / compliance** | failed-auth rate, unusual egress, unpatched CVEs, MFA coverage | **P** on anomaly, **N** on hygiene |
| 11 | **Cost** | daily cloud spend, cost per request, anomaly detection | **N** (budget overrun) |
| 12 | **People / toil** | pages/SRE/week, after-hours pages, toil hours/week | **D** (reviewed monthly) |
| 13 | **AI agents** *(if used)* | acceptance rate, false-correlation rate, time-to-context saved | **D** (`40-agents/evals/`) |

## Definition of done (per service)

A service in `{{services}}` is covered when all are true:

- [ ] Overview + service dashboard exist in {{stack.metrics}}
- [ ] RED metrics charted with percentiles
- [ ] At least one SLO with a burn-rate alert (see `10-slos/`)
- [ ] Saturation metric for its critical resource (USE)
- [ ] Dependency health visible (row 8)
- [ ] Every alert has owner + runbook (`20-alerting/alert-audit.csv`)
- [ ] Deploy/rollback events overlaid on the dashboard
- [ ] Named service owner in the roster

## Coverage review (quarterly, 30 min)

1. Walk this table top to bottom — mark gaps, assign owners
2. Compare against `{{services}}` and any new service added this quarter
3. Check layers 9–13: delivery, security, cost, toil, agents are the ones
   silently neglected
4. Output → gaps become backlog items, not notes nobody reads

## Prioritization when everything is a gap

**Layer 1 → 3 → 5 → 7** first: journeys, services, async, infra. Those four
cover the outage classes that page people at 3am. Business, cost and AI
metrics can wait one quarter; they can't cause an incident.
