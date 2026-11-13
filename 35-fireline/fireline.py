#!/usr/bin/env python3
"""Build this week's Fireline: rotation, channel banner and Monday agenda.

    python3 35-fireline/fireline.py                 # this ISO week
    python3 35-fireline/fireline.py --week 47       # a specific week
    python3 35-fireline/fireline.py --init          # create roster.csv from kit.yaml

Rotation: for each team in kit.yaml `teams`, pick person (week_index % rows).
Edit 35-fireline/roster.csv as people join/leave the rotation.
"""
import argparse
import csv
import datetime
import pathlib
import sys

import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from generate import parse_simple_yaml  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROSTER = pathlib.Path(__file__).with_name("roster.csv")


def init_roster() -> None:
    cfg = parse_simple_yaml((ROOT / "kit.yaml").read_text(encoding="utf-8"))
    teams = cfg.get("teams") or ["SRE", "QA", "Data"]
    if isinstance(teams, str):
        teams = [teams]
    with ROSTER.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["team", "person"])
        for t in teams:
            w.writerow([t, ""])
    print(f"created {ROSTER} — fill in one (or more) names per team")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--week", type=int, default=None, help="ISO week (default: current)")
    ap.add_argument("--init", action="store_true", help="create roster.csv from kit.yaml")
    args = ap.parse_args()

    if args.init or not ROSTER.is_file():
        init_roster()
        return 0

    with ROSTER.open(newline="", encoding="utf-8-sig") as f:
        roster = [r for r in csv.DictReader(f) if (r.get("person") or "").strip()]
    if not roster:
        print(f"roster empty — edit {ROSTER}", file=sys.stderr)
        return 1

    today = datetime.date.today()
    week = args.week or today.isocalendar().week
    by_team: dict[str, list[str]] = {}
    for r in roster:
        by_team.setdefault(r["team"], []).append(r["person"].strip())

    idx = week - 1
    picks = {t: names[idx % len(names)] for t, names in by_team.items()}
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)

    print(f"FIRELINE — week {week} ({monday} → {sunday})")
    print("=" * 60)
    for team, person in picks.items():
        print(f"  {team:10} → {person}")
    leader = next(iter(picks.values()))

    banner = [
        f":fire: *Fireline week {week}* ({monday} → {sunday})",
        "*On the front door:*",
        *[f"• {t}: {p}" for t, p in picks.items()],
        f"*Team leader:* {leader}",
        "_Qualify fast, solve same-day, everything else escapes to the owning "
        "team's backlog. Blocker = wakes someone at 3am — think twice._",
    ]
    print("\n--- post to #fireline ---")
    print("\n".join(banner))

    agenda = f"""MONDAY FIRELINE MEETING — week {week}
1. Handover: ongoing tickets from last week (outgoing team)
2. Confirm this week's roster: {', '.join(f'{t}={p}' for t, p in picks.items())}
3. Release previous week's tickets in the tracker
4. Blockers / repeat offenders → candidates for the alert audit
5. Leader: {leader} — owns qualification quality for the week
"""
    print("\n--- agenda ---")
    print(agenda)
    return 0


if __name__ == "__main__":
    sys.exit(main())
