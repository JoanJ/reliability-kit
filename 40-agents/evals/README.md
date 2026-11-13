# Agent evals — prove the agents earn their keep

Agents that aren't measured get quietly abandoned (or quietly trusted when
they shouldn't be). Four numbers, tracked manually in a spreadsheet is fine.

## The four metrics

| Metric | How to measure | Healthy signal |
|---|---|---|
| **Triage acceptance rate** | % of agent briefs a responder used without rewriting the conclusion | >60% |
| **Time-to-context** | Minutes from alert to "responder has the full picture" | −50% vs baseline |
| **Postmortem edit distance** | % of the draft that survived human review unchanged | >50% kept |
| **False correlation rate** | % of briefs that pointed at the wrong cause | <20% |

## Baseline first

Before enabling anything, measure the same numbers for **two weeks without
the agent** (time-to-context, postmortem writing time). Without a baseline,
improvement is a feeling.

## Procedure

1. Pick **one** service from `{{services}}` as the pilot
2. Run with read-only prompts for 2 weeks
3. Log every case in the eval sheet: input, output, human verdict, what was wrong
4. Review with the team: keep / adjust prompt / disable
5. Only then widen to more services — and re-measure

## Failure cases worth keeping forever

Collect them in `failures.md` (one line each):

```
2026-11-12 | triage | blamed the DB, was a deploy 4 min earlier | add deploy-window check
```

A small, honest failure log is the most valuable file in this folder.

## When to turn an agent off

- Acceptance rate below 40% after two tuning rounds
- Any incident where the agent's output contributed to a wrong decision
  → disable, run the blameless postmortem, treat it as a system condition
- Kill switch untested for a quarter
