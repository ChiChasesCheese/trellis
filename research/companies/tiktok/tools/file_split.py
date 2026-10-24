"""Move the split cards (`tlc-<slug>-<1..5>-*.md`) of finished problems from the whole-answer deck's folder into the
drill deck's folder. Whole-answer cards (`-0-whole`) stay. Only problems that already have their whole card move.

    uv run python research/companies/tiktok/tools/file_split.py [--dry-run]
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "vault/interviews/core/leetcode/tiktok/cards"
DST = ROOT / "vault/interviews/core/leetcode/tiktok-drill/cards"
SPLIT = re.compile(r"^(tlc-.+)-([1-5])-[a-z]+\.md$")


def main(argv: list[str]) -> int:
    moved = 0
    for branch in ("a", "b"):
        folder = SRC / branch
        if not folder.is_dir():
            continue
        whole = {p.name[: -len("-0-whole.md")] for p in folder.glob("*-0-whole.md")}
        for p in sorted(folder.glob("tlc-*.md")):
            m = SPLIT.match(p.name)
            if not m or m.group(1) not in whole:
                continue
            dest = DST / branch / p.name
            if "--dry-run" not in argv:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(p, dest)
            moved += 1
    print(f"{moved} split card(s) {'would move' if '--dry-run' in argv else 'moved'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
