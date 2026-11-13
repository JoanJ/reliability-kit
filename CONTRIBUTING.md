# Contributing

Thanks — PRs are how this kit stays true instead of theoretical.

## Most welcome

- **Real-world examples**: anonymized configs, filled-in worksheets, postmortem
  skeletons from actual incidents (no company data, no customer data)
- **New stack presets**: Datadog, Opsgenie, Sentry, Grafana Cloud — as
  examples, not as dependencies
- **Fixes to wrong assumptions**: if a template doesn't fit your org size or
  culture, say so and propose the variant
- **Prompt and eval improvements** for `40-agents/` — include a failure case
  if you have one

## Less welcome

- Frameworks, dependencies, build steps — this stays stdlib-only and runs in
  30 seconds
- Vendor-specific sales content
- Anything requiring signup to be useful

## Rules for changes

1. `python3 generate.py --check` must pass
2. Don't invent `{{placeholder-name}}` tokens that aren't in `kit.yaml`
3. Every template must stay readable in one sitting
4. Guardrail references (`40-agents/guardrails.md`) must stay correct —
   the AI policy is the product
5. Anonymize ruthlessly: no real company names, incidents, or people

## Pull request template

```markdown
## What changed
## Why
## How I validated it (generate.py --check / used it at my company)
## Anonymization confirmed: [ ]
```

## Conduct

Be kind in reviews. People are documenting their worst days at work when they
contribute incident material.
