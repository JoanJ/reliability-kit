#!/usr/bin/env python3
"""SLO / error-budget calculator.

    python3 10-slos/slo_calc.py --slo 99.9 --total 1000000 --failed 42
    python3 10-slos/slo_calc.py --slo 99.9 --total 1000000 --failed 42 --elapsed-hours 12

Prints: measured SLI, failures allowed vs used, budget remaining, and (with
--elapsed-hours) the burn rate — the number the error-budget policy reacts to.
"""
import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slo", type=float, required=True, help="target percent, e.g. 99.9")
    ap.add_argument("--total", type=float, required=True, help="total requests/events")
    ap.add_argument("--failed", type=float, required=True)
    ap.add_argument("--window-hours", type=float, default=30 * 24,
                    help="SLO window in hours (default: 30 days)")
    ap.add_argument("--elapsed-hours", type=float, default=None,
                    help="hours elapsed in the window so far")
    args = ap.parse_args()

    if args.total <= 0 or not 0 < args.slo < 100 or args.failed < 0:
        print("invalid inputs: need total>0, 0<slo<100, failed>=0", file=sys.stderr)
        return 2

    sli = 100 * (args.total - args.failed) / args.total
    allowed = args.total * (1 - args.slo / 100)
    used_pct = 100 * args.failed / allowed if allowed else float("inf")
    remaining = max(0.0, 100 - used_pct)

    print(f"measured SLI : {sli:.4f}%   (target {args.slo}%)")
    print(f"failures     : {args.failed:.0f} of {args.total:.0f} allowed "
          f"({allowed:.1f})")
    print(f"budget used  : {used_pct:.1f}%   remaining: {remaining:.1f}%")

    if args.elapsed_hours:
        burn = used_pct / (args.elapsed_hours / args.window_hours * 100)
        print(f"burn rate    : {burn:.1f}x  (1.0 = budget exhausted exactly on time)")
        print("  < 1.0 on track · 1–5x watch · > 6x fast burn → policy kicks in "
              "(10-slos/error-budget-policy.md)")

    # verdict against the policy
    verdict = ("OK — ship normally" if remaining > 25 else
               "WATCH — feature freeze needs go/no-go" if remaining > 10 else
               "PAUSE — releases frozen for this service" if remaining > 0 else
               "EXHAUSTED — declare sev-2, plan within 24h")
    print(f"verdict      : {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
