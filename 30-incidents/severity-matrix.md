# Severity matrix — {{company}}

One matrix, agreed once, used by everyone. If two people disagree on the
severity during an incident, **the higher one wins** and you re-triage later.

| | **Sev-1** | **Sev-2** | **Sev-3** | **Sev-4** |
|---|---|---|---|---|
| **Impact** | Total outage of a critical journey (`{{services}}`) or data loss/corruption | Major degradation; workaround exists | Partial impact to a subset of users | Cosmetic / internal only |
| **Users affected** | All | Significant subset | Small subset | None |
| **Revenue / legal** | Direct revenue loss, contractual breach, data exposure | Revenue at risk, SLA threatened | Negligible | None |
| **Response time** | Immediate | <15 min | Next business hour | Next sprint |
| **Who** | Incident commander + {{contact}} | IC + service owner | Service owner | Backlog |
| **Comms** | Status page + updates every 30 min | Status page on request | Internal only | None |
| **Postmortem** | Yes, blameless, ≤5 days | Yes, blameless, ≤10 days | Optional | No |
| **Pages** | Yes | Yes | Business hours only | Never |

## Assigning severity

1. Start from **user impact**, not from how loud the alert is
2. Unsure? Declare higher, announce the assumption, re-triage in 15 minutes
3. Severity can be lowered mid-incident; raising it re-triggers comms duties
4. The incident commander owns the call — during the incident there is no
   committee

## Incident roles

| Role | Responsibility |
|---|---|
| **Incident commander** | Runs the incident, calls severity, owns comms cadence — *not* the person fixing it |
| **Ops lead** | Coordinates the fix, tracks actions |
| **Comms lead** | Status page, stakeholder updates (Sev-1/2) |
| **Scribe** | Captures the timeline — feeds `40-agents/prompts/postmortem-draft.md` |

## Escalation

`{{stack.paging}}` → service owner (15 min) → {{contact}} (Sev-1/2) →
exec sponsor (Sev-1 > 1h)

> If you run a rotating front-door team for intake, tickets enter there first:
> see `35-fireline/intelligent-swarming.md`.

## Declaring an incident

```
INCIDENT | sev-2 | <service> | <one-line symptom> | IC: <name> | bridge: <link>
```
Post it where your team already talks. The bridge opens first, roles fill in
30 seconds later — speed over ceremony.
