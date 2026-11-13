# AI guardrails — {{company}}

**Policy:** `ai_policy: {{ai_policy}}` · **Owner:** {{contact}} · **Review:** quarterly

This document is part of the product, not an appendix. If your agents don't
follow it, they don't ship.

## The ladder of autonomy

| Setting | Agents may | Agents may never |
|---|---|---|
| `read-only` | Read logs, metrics, deploys; summarize; draft | Write anything anywhere; page anyone |
| `human-approval-required` | Above, plus propose actions (restart, scale, rollback) behind an approval gate | Execute without an explicit human click; act outside the approved list |
| `auto-remediate-safe-subset` | Above, plus execute pre-approved, idempotent, reversible actions within a blast-radius limit | Touch data stores, auth, billing, or anything outside the approved list |

Current: **`{{ai_policy}}`**

## Non-negotiables

1. **Read-only by default.** Write access is granted per-action, never per-role
2. **Approval gates are real.** One click from a named human, not a "reviewed
   by agent" checkbox
3. **Blast radius is defined in advance** — max instances, max services, max
   duration per autonomous action
4. **Everything is logged** — prompt, context, output, approver, action,
   result. Audit-ready, retained like any other production log
5. **No agent owns severity or "resolved".** Those are human calls
6. **No production data in prompts** beyond what the responder could already
   see; customer data is redacted at the source
7. **Kill switch exists** and is tested — one flag disables all agent actions

## Approval-gate pattern

```
agent proposes → shows evidence + blast radius → human approves/rejects
                → action executed with timeout → result logged → post-incident review
```

Rejects are feedback: they feed `evals/`, they are not a failure of the agent.

## Incident-time rules

- An agent may join the bridge as a **scribe/context provider**
- It may not declare severity, resolve the incident, or communicate externally
- If the agent's output is wrong, the responder says so in the timeline —
  that becomes an eval case

## Review & accountability

- Quarterly review with {{contact}}: eval trends, near-misses, kill-switch test
- Any incident where agent output contributed → normal blameless postmortem,
  agent behavior listed as a system condition
- New action types added to the approved list require the same review as any
  production change

## If you're a regulated or high-risk org

Set `ai_policy: read-only` and stop there. The prompts in `prompts/` still
work — they just don't propose actions. Nothing in this kit requires write
access to be useful.
