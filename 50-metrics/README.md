# Metrics — what we measure, and the rules for measuring it

One place where "what we measure and why" lives for {{company}}. If a metric
isn't here, it isn't officially watched.

| File | Contents |
|---|---|
| [`definitions.md`](definitions.md) | Precise definitions + formulas: golden signals, RED, USE, DORA, SLO/burn, incident and toil metrics |
| [`rules.md`](rules.md) | The rules every metric, dashboard and alert must obey |
| [`coverage.md`](coverage.md) | What to cover, layer by layer — the coverage checklist |

## The four questions (before any metric ships)

1. **Who looks at it?** (named owner, or it's decorative)
2. **What does a bad value mean?** (threshold with a reason, not a vibe)
3. **What action does it trigger?** (if none → dashboard, never a page)
4. **Is it a symptom or a cause?** (pages are for symptoms users feel)

## Cadence

| When | What | Where |
|---|---|---|
| Continuous | Dashboards + burn alerts | {{stack.metrics}} → {{stack.paging}} |
| Weekly | Pages/SRE, alert quality, overdue actions | Ops review |
| Monthly | The report below + SLO review | `10-slos/` agenda |
| Quarterly | DORA trend, dead-metric audit, alert audit | `20-alerting/alert-audit.csv` |

## Monthly report template

```
RELIABILITY {{company}} — <month>
Pages/SRE/week:      <n>   (target −50%)
Alerts actionable:   <n>%  (target 100%)
SLO coverage:        <n> of {{services}}
MTTR sev-1/2:        <n> min (target −30%)
Postmortem actions:  <n>% closed ≤30d (target 80%)
Burn:                <budget remaining per service>
Toil:                <h/week, from the alert audit>
```

Targets come from `00-program/90-day-plan.md`; numbers come from
`definitions.md` — no metric in this report is defined anywhere else.
