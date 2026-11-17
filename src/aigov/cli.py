from __future__ import annotations

import argparse
import sys

from .assess import RESPONSE, load, severity


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aigov", description="AI use-case risk tiering and incident severity")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assess", help="tier use cases from a JSON intake file")
    a.add_argument("file")
    i = sub.add_parser("incident", help="classify an incident")
    for flag in ("harm", "exposed", "repeated", "contained"):
        i.add_argument(f"--{flag}", action="store_true")
    args = p.parse_args(argv)

    if args.cmd == "assess":
        try:
            for r in load(args.file):
                print(f"{r.name}: tier={r.tier} score={r.score} approver={r.approver}")
                for c in r.controls:
                    print(f"   - {c}")
        except (ValueError, KeyError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        return 0
    sev = severity(args.harm, args.exposed, args.repeated, args.contained)
    print(f"{sev}: {RESPONSE[sev]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
