# Metric rules

Ten rules. Break one and the dashboard becomes decoration — or worse, the
alert becomes noise. Definitions: [`definitions.md`](definitions.md).

1. **Every metric has an owner and an action.** No owner → it's a graph, not
   a signal. No action → it never pages.

2. **Alert on symptoms users feel; notify on causes.** Error rate climbing =
   page. Disk filling = notify (it will show up as the symptom soon enough).
   Exception: a cause with a *faster* symptom path (cert expiry) pages.

3. **Percentiles, never averages.** Averages hide the 2% of users having a
   terrible day. Use histograms, chart p95/p99.

4. **Cardinality budget.** Label by low-cardinality dimensions only
   (service, region, route). **Never** `user_id`, `order_id`, `email`, full
   URLs — one label value per row is how a metrics backend dies.

5. **Naming and units are contracts.**
   - Base units: `_seconds` (not `_ms`), `_bytes` (not `_kb`)
   - Counters end in `_total`, gauges describe a current value
   - `http_requests_total{service,route,status}` — if you can't say what a
     label means in three words, drop it

6. **One overview, one per service, one per resource.** An overview dashboard
   answers "is it broken?" in 10 seconds; the service dashboard answers
   "where?" in 60. No dashboard needs more than a screen and a half.

7. **Thresholds come from SLOs, not vibes.** If it can't be tied to an error
   budget or a documented capacity limit, it's a dashboard line, not an alert.

8. **Every alert links to a runbook and an owner.** No runbook → not a page.
   Enforced by the quarterly audit in `20-alerting/alert-audit.csv`.

9. **Dead metrics get deleted quarterly.** Nobody has looked at it in 90 days?
   Delete it. A metric nobody uses still costs ingest, storage and attention.

10. **Pick the right tool.** Metrics answer "how much/how often", logs answer
    "what happened", traces answer "where in the call path". Don't build a
    logging pipeline to answer a metrics question — and don't infer a root
    cause from a graph alone.

## Anti-patterns

- ❌ Alerting on CPU/memory with no user-impact link
- ❌ "Dashboard of everything" — 40 panels, no question answered
- ❌ SLOs measured with a different query than the alert
- ❌ A metric defined in three places with three different numbers
- ❌ Team KPIs that reward silence (fewer alerts ≠ fewer problems)

## AI-assisted metrics (optional)

Under `ai_policy: {{ai_policy}}`, an agent may summarize burn drivers or
anomaly context for the monthly review. It may not change thresholds, create
alerts, or declare a metric healthy. Guardrails: `40-agents/guardrails.md`.
