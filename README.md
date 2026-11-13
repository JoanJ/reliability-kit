# Reliability Kit

**The reliability program for any company — templates, SLOs, alerting, incident process, plus AI agents that do the boring parts. Copy it, adapt it, ship it in a weekend.**

MIT licensed. No signup, no SaaS, no dependencies.

## Why this exists

Most teams don't have a reliability problem, they have a *definition* problem:
everything becomes an alert, every incident is ad-hoc, and nobody can prove
whether things are getting better. This kit is the 90-day program that fixes
all three at once.

## Quickstart

```bash
git clone <this-repo> && cd reliability-kit
$EDITOR kit.yaml          # 15 questions about your team
python3 generate.py --check
ls output/                # every template, filled with YOUR values
```

Requires Python 3.8+. Nothing else.

## Commands — the kit runs, it doesn't just describe

| Command | What it does |
|---|---|
| `python3 generate.py --check` | Render every template with your `kit.yaml` |
| `python3 incident.py --severity sev-2 --service checkout --summary "5xx spike"` | **Declare an incident**: creates the pre-filled postmortem (title, date/hour, participants, timeline), the Slack banner and the channel name — posts to Slack automatically if `SLACK_BOT_TOKEN`/`SLACK_WEBHOOK_URL` is set, and adds the bridge from `meeting_room` |
| `python3 20-alerting/alert_audit.py` | Score every alert: keep / downgrade / kill + pages-per-week summary (`--write` saves decisions) |
| `python3 35-fireline/fireline.py` | This week's Fireline rotation from `roster.csv` → `#fireline` banner + Monday agenda (`--init` to create the roster) |
| `python3 10-slos/slo_calc.py --slo 99.9 --total 1000000 --failed 42` | SLI, budget used/remaining, burn rate, and the policy verdict (OK / watch / freeze / exhausted) |
| `python3 50-metrics/report.py` | Monthly reliability report computed from the kit's own CSVs, with overdue actions listed |

All scripts are stdlib-only, fail loudly, and leave a `--selftest` where the
logic is non-trivial (`incident.py --selftest`).

## What's inside

| Folder | Contents |
|---|---|
| `00-program/` | The 90-day rollout plan — phases, owners, metrics to report |
| `10-slos/` | SLI/SLO worksheet, error-budget policy, review agenda |
| `20-alerting/` | Alert audit spreadsheet (with scoring), on-call policy |
| `30-incidents/` | Severity matrix, blameless postmortem template, action tracker |
| `35-fireline/` | **Fireline / Intelligent Swarming** — one front door for incident intake |
| `40-agents/` | **AI layer**: prompts, agent definitions, guardrails, evals |
| `50-metrics/` | DORA / RED / USE queries and dashboard definitions |
| `examples/` | A fully filled-in example config (`Acme Corp`) |

## How adaptation works

Everything renders from one file, [`kit.yaml`](kit.yaml):

```yaml
company: Acme Corp
team_size: 40
on_call: follow-the-sun
stack: { metrics: Grafana, paging: PagerDuty, incidents: Linear }
ai_policy: human-approval-required
services: [checkout, login, search]
```

Templates use `{{placeholder-name}}` tokens; `generate.py` substitutes them. A startup
with 5 engineers and a 500-person platform org both get a program that fits
them, with zero manual editing.

## The AI layer (`40-agents/`)

Agents that help with triage, postmortems, runbooks and SLO drafting — built
on four principles:

1. **Agents gather, humans decide** — the triage agent has logs, dashboards
   and recent deploys ready before the bridge opens; it never writes to prod
2. **Postmortem drafting, not postmortem writing** — a human owns the final text
3. **Read-only by default** — write access only behind an approval gate with
   a blast-radius limit, everything logged
4. **Evaluated like code** — `40-agents/evals/` measures acceptance rate,
   time saved and false correlations, so you can prove the agent earns its keep

Your `ai_policy` setting renders into the guardrails document and the agent
definitions, so the policy follows your company's risk tolerance.

## Principles

- Templates you can read in one sitting, not a framework
- Stdlib-only generator — a new user runs it in 30 seconds or they won't
- Works with your stack, not instead of it
- Every file is a starting point: fork it, break it, send it back

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs that add a real-world example,
fix a wrong assumption, or cover a new stack are the most welcome.

## License

[MIT](LICENSE) — use it commercially, no attribution required (a star is nicer).

## Sponsors

Sponsoring funds maintenance and early access to new modules. Companies that
would rather pay someone to roll this out: that's what the author does —
see "Implemented by" in the docs.
