# AGENTS.md — Reliability Kit ({{company}})

Instructions for AI agents working in this repository.

## What this repo is

The reliability program for {{company}}: 90-day plan, SLOs, alerting,
incident process, AI layer. Templates render from `kit.yaml` via
`python3 generate.py --check`.

## Hard rules

1. **Read `40-agents/guardrails.md` first.** The active policy is
   `ai_policy: {{ai_policy}}`. Never propose or execute actions beyond it
2. **Never write to production.** Reading logs/metrics/deploys is fine;
   proposing an action means marking it `[needs approval]`
3. **Never declare an incident resolved** or assign severity — humans do that
4. **Postmortems are drafts.** A human owns the final text; mark inferences `[?]`
5. **Don't break the generator.** Any template you edit must still render:
   run `python3 generate.py --check` before you finish, and keep
   `{{placeholder-name}}` syntax intact (keys must exist in `kit.yaml`)
6. **No secrets, no customer data** in templates, examples or prompts

## Conventions

- Templates are Markdown or CSV, one concern per file, readable in one sitting
- Placeholders: `{{your-key}}` or `{{nested.your-key}}` — flat config, one nesting level
- Dates/numbers are written for humans, not parsed by scripts
- Keep it dependency-free: Python stdlib only

## Definition of done for any change

- [ ] `python3 generate.py --check` passes
- [ ] No placeholder invented that isn't in `kit.yaml`
- [ ] Existing examples still make sense (`examples/example/kit.yaml`)
- [ ] Guardrail references still point at the right file
