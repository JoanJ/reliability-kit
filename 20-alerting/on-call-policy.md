# On-call policy — {{company}}

**Rotation:** `{{on_call}}` · **Engineering hours:** {{engineering_hours}} · **Timezone:** {{timezone}}
**Paging tool:** {{stack.paging}} · **Escalation contact:** {{contact}}

## Principles

1. Every page has an **action**. If nobody knows what to do when it fires,
   it is not a page — it is a notification
2. Every page has an **owner** (a team, not a person who left in March)
3. The person on call is **never the only one who can fix it** — runbooks
   exist so a new hire can act on day one
4. Paging outside agreed hours is an **incident, not a nudge**

## Rotation by team size

| Setup | Applies at {{team_size}} engineers | Cadence |
|---|---|---|
| `follow-the-sun` | 16+ | Regional rotations, ~5 days on, handover at 10:00 {{engineering_hours}} |
| `single-rotation` | 6–15 | One primary + one secondary, 7 days on / 7 off |
| `business-hours` | <6 | Pages outside hours auto-escalate to the on-call vendor or next-day queue |

Your current setting: **`{{on_call}}`**

## Severity → response

| Severity | Definition | Response | Who |
|---|---|---|---|
| Sev-1 | Customer-facing outage / data at risk | Immediate, all hands | IC + {{contact}} informed |
| Sev-2 | Major degradation, workaround exists | <15 min | IC + service owner |
| Sev-3 | Partial impact, internal | Next business hour | Service owner |
| Sev-4 | Cosmetic, no user impact | Next sprint | Backlog |

See `30-incidents/severity-matrix.md` for the full definitions.

## Compensation & wellbeing (non-negotiable)

- Time off in lieu for weekend/sev-1 work, taken within 2 weeks
- Max 5 consecutive days primary; secondary carries a full backup week
- A week with >8 pages triggers an alert-quality review — the *alerts* get
  reviewed, not the responder
- Every incident out of hours gets a follow-up in the weekly ops review

## Alert hygiene rules

- Any alert that pages twice with no action taken → auto-downgraded after review
- New pages require: owner, runbook link, threshold rationale
- Quarterly full audit: `20-alerting/alert-audit.csv`

## AI assistance

Under `ai_policy: {{ai_policy}}`, an agent may enrich incoming pages with
context (recent deploys, dashboards, likely cause) **before** the responder
opens the bridge. It does not acknowledge, silence or resolve pages on your
behalf. Details: `40-agents/guardrails.md`.
