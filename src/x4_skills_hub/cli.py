"""CLI entry for skills hub."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .validate import validate_tree
from .score import score_tree


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="x4-skills", description="X4 Agent Skills Hub")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="Validate skill directories")
    p_val.add_argument("--root", default="skills")

    p_score = sub.add_parser("score", help="Score skills and write registry")
    p_score.add_argument("--root", default="skills")
    p_score.add_argument("--out", default="registry/skills.json")

    p_report = sub.add_parser("report", help="Print summary report")
    p_report.add_argument("--registry", default="registry/skills.json")

    args = parser.parse_args(argv)

    if args.cmd == "validate":
        errors = validate_tree(Path(args.root))
        if errors:
            for e in errors:
                print(f"FAIL {e}", file=sys.stderr)
            return 1
        print("OK all skills valid")
        return 0

    if args.cmd == "score":
        records = score_tree(Path(args.root))
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"scored={len(records)} out={out}")
        return 0

    if args.cmd == "report":
        path = Path(args.registry)
        if not path.exists():
            print("registry missing — run score first", file=sys.stderr)
            return 1
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"skills={len(data)}")
        for r in data[:10]:
            print(f"  {r['name']}: quality={r['quality']} security={r['security']}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
