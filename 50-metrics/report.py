#!/usr/bin/env python3
"""Monthly reliability report — computed from the kit's own CSVs.

    python3 50-metrics/report.py                 # current month
    python3 50-metrics/report.py --month 2026-11

Reads:  30-incidents/action-tracker.csv  (action closure, overdue)
        20-alerting/alert-audit.csv      (pages/week, actionable %)
Prints: the report block from 50-metrics/README.md with real numbers.
Values that need external sources (SLO coverage, MTTR) are marked NEEDS SOURCE.
"""
import argparse
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read(path: pathlib.Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default=None, help="YYYY-MM (default: current)")
    args = ap.parse_args()

    today = datetime.date.today()
    month = args.month or today.strftime("%Y-%m")
    year, mon = (int(x) for x in month.split("-"))
    month_end = datetime.date(year, mon, 28) + datetime.timedelta(days=4)
    month_end = month_end - datetime.timedelta(days=month_end.day)

    actions = read(ROOT / "30-incidents" / "action-tracker.csv")
    alerts = read(ROOT / "20-alerting" / "alert-audit.csv")

    # --- actions ---
    closed = [a for a in actions if (a.get("status") or "").lower() in
              ("done", "closed", "verified")]
    overdue = [a for a in actions
               if a not in closed and a.get("due_date")
               and datetime.date.fromisoformat(a["due_date"]) < today]
    closure = f"{100 * len(closed) / len(actions):.0f}%" if actions else "n/a (0 actions)"

    # --- alerts ---
    if alerts:
        pages = sum(float(a.get("pages_per_week") or 0) for a in alerts)
        actionable = sum(float(a.get("actionable_pct") or 0) for a in alerts) / len(alerts)
        runbooks = 100 * sum(1 for a in alerts
                             if (a.get("has_runbook") or "").lower() == "yes") / len(alerts)
        alert_line = (f"{pages:.1f} total ({pages / 10:.1f}/SRE/week at 10 SREs)   "
                      f"actionable {actionable:.0f}%   with runbook {runbooks:.0f}%   "
                      f"alerts {len(alerts)}")
    else:
        alert_line = "NEEDS SOURCE — no rows in alert-audit.csv"

    report = f"""RELIABILITY REPORT — {month}
Pages/SRE/week:      {alert_line}
Alerts actionable:   {f'{actionable:.0f}%' if alerts else 'NEEDS SOURCE'}  (target 100%)
SLO coverage:        NEEDS SOURCE — from {ROOT.name}/10-slos worksheet
MTTR sev-1/2:        NEEDS SOURCE — from incident timelines
Postmortem actions:  {closure} closed   |   overdue: {len(overdue)}  (target 80% closed ≤30d)
Burn:                NEEDS SOURCE — from the SLO dashboard
Toil:                NEEDS SOURCE — estimate from the alert audit
"""
    print(report)

    if overdue:
        print("OVERDUE ACTIONS")
        for a in overdue:
            print(f"  [{a.get('due_date')}] {a.get('action')} — {a.get('owner') or 'NO OWNER'}")
        print()
    if actions and not closed:
        print("note: no action marked done/closed yet — status values I accept: "
              "done, closed, verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
