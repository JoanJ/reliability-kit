#!/usr/bin/env python3
"""Declare an incident: create the postmortem file + Slack banner, and post it.

    python3 incident.py --severity sev-2 --service checkout --summary "5xx spike"
    python3 incident.py --severity sev-1 --service login --summary "login down" \
        --ic NAME --participants "NAME, NAME2"

Creates:  incidents/INC-<date>-<time>-<slug>/postmortem.md   (pre-filled basics)
Prints:   the Slack banner + the channel name to open
Posts:    to Slack if SLACK_WEBHOOK_URL or SLACK_BOT_TOKEN is set

Meeting bridge: MEETING_URL env var, or `meeting_room` in kit.yaml.
Stdlib only.
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

from generate import parse_simple_yaml, render

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / "30-incidents" / "postmortem-template.md"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:40] or "incident"


def slack_api(method: str, token: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def slack_webhook(url: str, text: str) -> None:
    req = urllib.request.Request(
        url, data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=15).read()


def build_postmortem(cfg: dict, sev: str, service: str, summary: str,
                     ic: str, participants: str, now: datetime.datetime) -> str:
    """Fill the canonical template's basics — title, date/hour, participants."""
    text = render(TEMPLATE.read_text(encoding="utf-8"), cfg, set())
    local = now.strftime("%Y-%m-%d %H:%M")
    utc = now.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")

    text = re.sub(r"^# Postmortem — <incident title>$",
                  f"# Postmortem — {summary}", text, flags=re.M)
    text = text.replace("| **Severity** | Sev-? (see `severity-matrix.md`) |",
                        f"| **Severity** | {sev} |")
    text = re.sub(r"\| \*\*Date / duration\*\* \|[^|]*\|",
                  f"| **Date / duration** | {local} ongoing ({cfg.get('timezone', 'local')}) |",
                  text, count=1)
    text = re.sub(r"\| \*\*Incident commander\*\* \|[^|]*\|",
                  f"| **Incident commander** | {ic or '_assign now_'} |", text, count=1)
    text = re.sub(r"\| \*\*Author\(s\)\*\* \|[^|]*\|",
                  f"| **Author(s)** | {participants or '_assign now_'} |", text, count=1)
    text = text.replace("| **Services** | |", f"| **Services** | {service} |")
    text = re.sub(r"\| Time \(UTC\) \| Event \|\n\|---\|---\|\n",
                  "| Time (UTC) | Event |\n|---|---|\n"
                  f"| {utc} | Incident declared ({sev}) — {summary} |\n",
                  text, count=1)
    return text


def build_banner(cfg: dict, sev: str, service: str, summary: str,
                 channel: str, meet: str, pm_path: str, now: datetime.datetime) -> str:
    local = now.strftime("%H:%M")
    lines = [
        f":rotating_light: *INCIDENT DECLARED — {sev.upper()}*",
        f"*What:* {summary}",
        f"*Service:* {service}",
        f"*Declared:* {local} ({cfg.get('timezone', 'local')}) by "
        f"{cfg.get('contact', 'on-call')}",
        f"*Channel:* `{channel}`",
    ]
    if meet:
        lines.append(f"*Bridge:* {meet}")
    lines += [
        f"*Postmortem:* `{pm_path}`",
        f"_Severity per severity-matrix.md · IC to be named in the channel · "
        f"Comms every 30 min for sev-1/2_",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--severity", required=True,
                    choices=["sev-1", "sev-2", "sev-3", "sev-4"])
    ap.add_argument("--service", required=True, help="affected service")
    ap.add_argument("--summary", required=True, help="one-line symptom")
    ap.add_argument("--ic", default="", help="incident commander")
    ap.add_argument("--participants", default="", help="comma-separated")
    ap.add_argument("--no-slack", action="store_true", help="print only, never post")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    cfg = parse_simple_yaml((ROOT / "kit.yaml").read_text(encoding="utf-8"))
    now = datetime.datetime.now().astimezone()

    channel = f"inc-{now.strftime('%Y%m%d-%H%M')}-{slugify(args.service)}"
    slug = f"INC-{now.strftime('%Y%m%d-%H%M')}-{slugify(args.service)}"
    rel_path = f"incidents/{slug}/postmortem.md"

    pm = build_postmortem(cfg, args.severity, args.service, args.summary,
                          args.ic, args.participants, now)
    meet = os.environ.get("MEETING_URL") or cfg.get("meeting_room", "")
    banner = build_banner(cfg, args.severity, args.service, args.summary,
                          channel, meet, rel_path, now)

    if args.selftest:
        checks = {
            "title filled": f"# Postmortem — {args.summary}" in pm,
            "severity filled": f"| **Severity** | {args.severity} |" in pm,
            "date filled": "ongoing" in pm,
            "participants filled": (args.participants or "_assign now_") in pm,
            "timeline seeded": "Incident declared" in pm,
            "no placeholders": "{{" not in pm,
            "banner has channel": channel in banner,
        }
        bad = [k for k, v in checks.items() if not v]
        print("selftest:", "OK" if not bad else f"FAILED: {bad}")
        return 0 if not bad else 1

    out_dir = ROOT / "incidents" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "postmortem.md").write_text(pm, encoding="utf-8")
    (out_dir / "banner.txt").write_text(banner, encoding="utf-8")
    pm_path = out_dir / "postmortem.md"

    # --- Slack (optional, real automation when configured) ---
    if not args.no_slack:
        token = os.environ.get("SLACK_BOT_TOKEN")
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        try:
            if token:
                created = slack_api("conversations.create", token,
                                    {"name": channel, "is_private": False})
                if created.get("ok"):
                    slack_api("chat.postMessage", token,
                              {"channel": created["channel"]["id"], "text": banner})
                    print(f"slack: created #{channel} and posted the banner")
                else:
                    print(f"slack: channel not created ({created.get('error')}) — "
                          "banner not posted, use banner.txt", file=sys.stderr)
            elif webhook:
                slack_webhook(webhook, banner)
                print("slack: banner posted via webhook")
            else:
                print("slack: no SLACK_BOT_TOKEN / SLACK_WEBHOOK_URL — "
                      "copy banner.txt manually")
        except Exception as e:  # network/credential failure must not lose the incident
            print(f"slack: failed ({e}) — copy banner.txt manually", file=sys.stderr)

    print(f"\nchannel : #{channel}")
    if meet:
        print(f"bridge  : {meet}")
    else:
        print("bridge  : set MEETING_URL or `meeting_room` in kit.yaml")
    print(f"postmortem: {pm_path.relative_to(ROOT)}")
    print("\n" + banner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
