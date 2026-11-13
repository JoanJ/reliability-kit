# AI layer — agents for the reliability program

Everything here assumes one rule: **agents gather, humans decide.** Read
[`guardrails.md`](guardrails.md) before wiring anything into production.

## What's in here

```
40-agents/
├── prompts/                 # ready-to-use prompts, stack-agnostic
│   ├── alert-triage.md      # alert → context, likely cause, next step
│   ├── postmortem-draft.md  # timeline → blameless first draft
│   ├── runbook-generator.md # recurring ticket → runbook draft
│   └── slo-proposer.md      # service description → SLI/SLO draft
├── agents/
│   └── claude-code/         # AGENTS.md + skill definitions for agent IDEs
├── evals/                   # prove the agents actually help
└── guardrails.md            # policy that renders from {{ai_policy}}
```

## Where agents help today (2026 consensus)

| Task | Agent does | Human does | Typical saving |
|---|---|---|---|
| **Triage** | Pull logs, dashboards, last 5 deploys, SLO state into one view before the bridge opens | Decide cause, pick the fix | 5–15 min per incident |
| **Postmortem draft** | Build timeline from alerts/chat/PRs, write first draft | Own the final text, verify every line | 1–3 h per postmortem |
| **Runbook draft** | Turn a recurring ticket into a structured runbook | Validate steps against reality | 1 h per runbook |
| **SLO proposal** | Propose SLIs from available telemetry | Set the number, own the trade-off | days of negotiation |

## Where agents do **not** belong (yet)

- Writing to production, acknowledging or silencing pages unattended
- Deciding incident severity or declaring "resolved"
- Authoring the final postmortem — auto-written postmortems get gamed

## Adoption path

1. Start with **prompts only** — paste into whatever assistant your team uses
2. Add **read-only MCP access** to logs/dashboards so triage has real context
3. Add an **eval** (`evals/`) and measure for 2 weeks before trusting it
4. Only then consider write access, and only inside the blast-radius limits
   in `guardrails.md`

## Your policy

This kit renders your company's setting, currently:

> **`ai_policy: {{ai_policy}}`**

— it appears in the guardrails doc, the on-call policy, the postmortem
template and the agent definitions, so policy and practice can't drift apart.
