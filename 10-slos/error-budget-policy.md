# Error budget policy — {{company}}

**Owner:** {{contact}} · **Review cadence:** monthly · **Applies to:** {{services}}

## What an error budget is

If your SLO is 99.9%, the error budget is the 0.1% you're *allowed* to spend.
It converts reliability from an opinion into a number that product and
engineering can make trade-offs with.

## The policy

1. **Budget = 1 − SLO over the rolling window** (default 30 days)
2. **Burn alerts fire at 2% and 10% of budget in 1h / 6h / 3d windows**
   (multi-window, multi-burn-rate — see `50-metrics/`)
3. **Budget remaining ≥ 25%:** normal operation, ship as usual
4. **Budget 10–25%:** feature releases require an explicit go/no-go from the
   service owner; incident follow-ups get priority
5. **Budget < 10%:** **releases paused** for the affected service until the
   trend recovers. Only reliability work and approved hotfixes
6. **Budget exhausted:** sev-2 declared, service owner + {{contact}} notified,
   written plan within 24h
7. **Budget replenishes automatically** — no manual reset, no blame

## Guardrails against gaming

- Pausing releases is a **process pause, not a punishment**; postmortems stay
  blameless
- Changing the SLO to escape a freeze requires sign-off from the service
  owner **and** {{contact}}, and takes effect next window — never retroactively
- Repeated freezes in one quarter trigger a review of the *service*, not the
  people

## AI-assisted burn analysis

When `ai_policy` is set to `{{ai_policy}}` in `kit.yaml`, an agent may
summarize burn-rate drivers (recent deploys, traffic shifts, dependency
changes) for the monthly review. The agent **proposes; the owner decides.**
See `40-agents/guardrails.md`.
