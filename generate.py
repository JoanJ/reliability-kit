#!/usr/bin/env python3
"""Render every Reliability Kit template with the values in kit.yaml.

Stdlib only. Usage:
    python3 generate.py                  # render into ./output
    python3 generate.py --check          # render + fail on unreplaced {{placeholders}}
    python3 generate.py --config my.yaml --out /tmp/kit

The YAML reader is intentionally a minimal subset parser (flat keys, one
level of nesting, string lists) so there is nothing to install. If your
config needs more than that, keep it flat.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

TEMPLATE_DIRS = ("00-program", "10-slos", "20-alerting", "30-incidents", "35-fireline", "40-agents", "50-metrics")
PLACEHOLDER = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")


def scalar(v: str):
    """Strip quotes and trailing ` # comment` (put no # inside values)."""
    v = v.strip()
    head, sep, _ = v.partition(" #")
    if sep:
        v = head.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_simple_yaml(text: str) -> dict:
    """Flat keys + one level of nesting + string lists. See module docstring."""
    root: dict = {}
    top = None  # key whose block we are inside
    for raw in text.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())

        if s.startswith("- "):
            if top is None:
                raise ValueError(f"list item outside a key: {raw}")
            if root[top] is None:
                root[top] = []
            if not isinstance(root[top], list):
                raise ValueError(f"list inside a mapping: {raw}")
            root[top].append(scalar(s[2:]))
            continue

        if ":" not in s:
            raise ValueError(f"cannot parse line: {raw}")
        key, _, val = s.partition(":")
        key, val = key.strip(), val.strip()

        if indent == 0:
            top = key if val == "" else None
            root[key] = None if val == "" else scalar(val)
        else:
            if top is None:
                raise ValueError(f"indented line outside a key: {raw}")
            if root[top] is None:
                root[top] = {}
            if not isinstance(root[top], dict):
                raise ValueError(f"mapping inside a list: {raw}")
            root[top][key] = scalar(val)
    return root


def lookup(cfg: dict, path: str):
    cur = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def render(text: str, cfg: dict, missing: set) -> str:
    def sub(m):
        key = m.group(1)
        val = lookup(cfg, key)
        if val is None:
            missing.add(key)
            return m.group(0)
        if isinstance(val, list):
            return ", ".join(str(v) for v in val)
        return str(val)

    return PLACEHOLDER.sub(sub, text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="kit.yaml")
    ap.add_argument("--out", default="output")
    ap.add_argument("--check", action="store_true", help="fail if any {{placeholder}} is left")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent
    cfg_path = Path(args.config)
    if not cfg_path.is_file():
        cfg_path = root / args.config
    if not cfg_path.is_file():
        print(f"config not found: {args.config}", file=sys.stderr)
        return 2

    cfg = parse_simple_yaml(cfg_path.read_text(encoding="utf-8"))

    out_root = Path(args.out)
    if out_root.exists():
        shutil.rmtree(out_root)

    missing: set = set()
    rendered = 0
    for d in TEMPLATE_DIRS:
        src = root / d
        if not src.is_dir():
            continue
        for f in sorted(src.rglob("*")):
            if f.is_dir():
                continue
            rel = f.relative_to(root)
            if f.suffix not in {".md", ".csv", ".txt", ".yaml", ".yml"}:
                continue  # scripts and binaries are not templates
            dst = out_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            text = f.read_text(encoding="utf-8")
            text = render(text, cfg, missing)
            dst.write_text(text, encoding="utf-8")
            rendered += 1

    print(f"rendered {rendered} files -> {out_root}/")

    if missing:
        print(f"undefined placeholders: {', '.join(sorted(missing))}", file=sys.stderr)
        return 1

    if args.check:
        leftovers = [
            str(p.relative_to(out_root))
            for p in out_root.rglob("*")
            if p.is_file() and PLACEHOLDER.search(p.read_text(encoding="utf-8", errors="ignore"))
        ]
        if leftovers:
            print("unreplaced placeholders in: " + ", ".join(leftovers), file=sys.stderr)
            return 1
        print("check OK: no unreplaced placeholders")
    return 0


if __name__ == "__main__":
    sys.exit(main())
