# 90-day reliability program — {{company}}

> Rendered by Reliability Kit · {{team_size}} engineers · hours {{engineering_hours}}
> Paging: {{stack.paging}} · Metrics: {{stack.metrics}} · Incidents: {{stack.incidents}}

**The pitch in one sentence:** cut alert noise in half, put numbers behind
reliability, and make incidents produce actions that actually close — in one quarter.

## Why these three, together

Alert noise, missing SLOs and messy incidents share one root cause: no agreed
definition of reliability. Fixing them separately wastes effort; as one
program they share the same data.

## Phase 1 — Weeks 1–4: Alert & on-call audit *(the fast win)*

- [ ] Inventory every alert: source, threshold, owner, actionability, paged
      someone in the last 90 days
- [ ] Kill or downgrade anything with no defined action; dedupe overlaps
- [ ] Publish the "before" number: alerts/week, pages/SRE/week, % actionable
- [ ] Publish the on-call policy (`20-alerting/on-call-policy.md`), rotation
      matching your setup: `{{on_call}}`

**Exit criteria:** alert set reduced ≥50%, every surviving alert has an owner
and a documented action.

## Phase 2 — Weeks 3–6: SLO baseline *(the numbers)*

- [ ] Pick the critical user journeys: `{{services}}`
- [ ] Define SLIs from data you already have; set SLOs (see `10-slos/`)
- [ ] Publish the reliability dashboard
- [ ] Adopt the error-budget policy — what pauses releases when burn is high

**Exit criteria:** SLOs live for every listed service, dashboard visible to
engineering leadership.

## Phase 3 — Weeks 5–10: Incident process *(the mess)*

- [ ] Adopt the severity matrix (`30-incidents/severity-matrix.md`)
- [ ] Assign one incident commander per sev-1/2
- [ ] Run blameless postmortems from the template; every action gets a named
      owner and a due date — tracked in `30-incidents/action-tracker.csv`
- [ ] Weekly ops review closes or reassigns overdue actions

**Exit criteria:** first 3 postmortems written, 100% of actions assigned.

## Phase 4 — Weeks 9–12: Close the loop

- [ ] Report before/after to leadership (table below)
- [ ] Institutionalize the rituals: quarterly alert review, monthly SLO
      review, action-item audit

## Metrics to report monthly

| Metric | Baseline (week 1) | Target (week 12) |
|---|---|---|
| Pages per SRE per week | _measure_ | −50% |
| % alerts with a documented action | _measure_ | 100% |
| Critical journeys with SLOs | 0 | {{services}} covered |
| Postmortem actions closed ≤30 days | _measure_ | ≥80% |
| MTTR (top 2 severities) | _measure_ | −30% |

## How to run it with {{team_size}} engineers

- **Don't run it alone.** Recruit 3–4 senior engineers as a part-time tiger
  team (20% time each), one per phase — this also builds your next leaders
- **Steering check-in:** 30 min every two weeks with one exec sponsor.
  Show the dashboard, not slides
- **Frame it as "fewer useless pages, more sleep"** — on-call pain is your
  best recruiting tool for internal support

## What kills this program

- Alerting on everything "just in case" → make the alert budget explicit
- SLOs on infrastructure with no identifiable user → start from user journeys
- Postmortems with actions nobody owns → no owner, no due date, no close
- Treating `ai_policy: {{ai_policy}}` as a suggestion → the guardrails are
  part of the product

## First week, literally

1. Pull 90 days of page history from {{stack.paging}}
2. Get the exec sponsor to agree on the metrics above
3. Name the services you'll SLO: `{{services}}`
4. Announce the program + recruit the tiger team
