# Postmortem — <incident title>

| | |
|---|---|
| **Severity** | Sev-? (see `severity-matrix.md`) |
| **Date / duration** | YYYY-MM-DD, HH:MM–HH:MM ({{timezone}}) |
| **Services** | |
| **Incident commander** | |
| **Author(s)** | |
| **Status** | draft / reviewed / actions-closed |

> Blameless rule: we describe **what the system allowed**, never who failed.
> If a human action was involved, ask what made that action reasonable at the time.

## 1. Summary (3–5 sentences)

_What happened, who was affected, what we did about it._

## 2. Impact

- Users affected: _
- Duration of user-facing impact: _
- Revenue / contractual impact: _
- Data integrity: _none / verified clean / at risk_

## 3. Timeline (UTC + {{timezone}})

| Time (UTC) | Event |
|---|---|
| | First signal (alert, customer report, dashboard) |
| | Incident declared, severity assigned |
| | IC assigned, bridge opened |
| | Root cause identified |
| | Mitigation applied |
| | User impact ended |
| | Incident resolved |

_Draft this section with `40-agents/prompts/postmortem-draft.md` — paste the
alert/chat/PR timeline, review every line, delete what's wrong. The agent
drafts; a human owns the final text._

## 4. Root cause

_The "why" behind the "why". Five whys, stop when you reach something a
process or design can fix — never "human error"._

## 5. What went well

-

## 6. What went poorly

-

## 7. Where we got lucky

_

## 8. Actions

| # | Action | Owner | Due | Tracker row | Status |
|---|---|---|---|---|---|
| 1 | | | | `action-tracker.csv` | open |
| 2 | | | | | open |

Rules: **no owner → not an action**; **no due date → not an action**; every
row lives in `30-incidents/action-tracker.csv` and is reviewed weekly.

## 9. Detection

| Question | Answer |
|---|---|
| How was it detected? | alert / customer / human |
| Time to detect | |
| Could an agent have caught it earlier? | _see `ai_policy: {{ai_policy}}`_ |

## Sign-off

- [ ] Timeline verified by IC
- [ ] Actions assigned with due dates
- [ ] Reviewed in ops review (date: )
- [ ] Actions closed and verified (date: )
