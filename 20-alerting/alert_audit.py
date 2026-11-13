#!/usr/bin/env python3
"""Score the alert audit and suggest keep / downgrade / kill decisions.

    python3 20-alerting/alert_audit.py              # print scoring + summary
    python3 20-alerting/alert_audit.py --write      # also update the decision column

Scoring (see 50-metrics/rules.md: every alert needs owner, runbook, action):
    actionable < 30%                      -> kill
    actionable < 70%  or  no runbook      -> downgrade
    otherwise                             -> keep
"""
import argparse
import csv
import pathlib
import sys

CSV_PATH = pathlib.Path(__file__).with_name("alert-audit.csv")


def score(row: dict) -> tuple[str, str]:
    actionable = float(row.get("actionable_pct") or 0)
    runbook = (row.get("has_runbook") or "").lower() == "yes"
    pages = float(row.get("pages_per_week") or 0)
    if actionable < 30:
        return "kill", f"only {actionable:.0f}% of firings are actionable"
    if actionable < 70:
        return "downgrade", f"{actionable:.0f}% actionable (<70%)"
    if not runbook:
        return "downgrade", "no runbook linked" + (" and it pages" if pages else "")
    if pages > 0 and not row.get("owner"):
        return "downgrade", "pages but has no owner"
    return "keep", "actionable, runbook, owner"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", default=str(CSV_PATH))
    ap.add_argument("--write", action="store_true", help="update the decision column")
    args = ap.parse_args()

    path = pathlib.Path(args.csv)
    if not path.is_file():
        print(f"not found: {path}", file=sys.stderr)
        return 2
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("empty audit — fill it from a 90-day export of your paging tool")
        return 0

    total_pages = 0.0
    counts = {"keep": 0, "downgrade": 0, "kill": 0}
    print(f"{'alert':28} {'pages/wk':>8} {'act%':>5} {'runbook':>7}  decision")
    print("-" * 78)
    for row in rows:
        decision, why = score(row)
        counts[decision] += 1
        total_pages += float(row.get("pages_per_week") or 0)
        print(f"{(row.get('name') or '?')[:28]:28} "
              f"{float(row.get('pages_per_week') or 0):8.1f} "
              f"{float(row.get('actionable_pct') or 0):5.0f} "
              f"{(row.get('has_runbook') or '-'):>7}  {decision} — {why}")
        if args.write and "decision" in row:
            row["decision"] = decision

    n = len(rows)
    pct = lambda pred: 100 * sum(1 for r in rows if pred(r)) / n
    print("-" * 78)
    print(f"alerts: {n}   pages/week: {total_pages:.1f}   "
          f"keep {counts['keep']} / downgrade {counts['downgrade']} / kill {counts['kill']}")
    print(f"actionable ≥70%: {pct(lambda r: float(r.get('actionable_pct') or 0) >= 70):.0f}%   "
          f"with runbook: {pct(lambda r: (r.get('has_runbook') or '').lower() == 'yes'):.0f}%")

    if args.write:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"decisions written to {path}")
    else:
        print("(run with --write to save the decisions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
