"""cd05 Business Account Data Verification — YOUR implementation."""

from __future__ import annotations

import json
import sys


def part1(doc: dict) -> list[str]:
    """doc = {"account": {...}, "rules": [...]}. Part 1 rules only have "requires" (dot paths,
    no "[]" wildcards, no "when"). Return sorted, de-duplicated missing paths, or ["VERIFIED"]."""
    # TODO
    return []


def part2(doc: dict) -> list[str]:
    """Same as part1, plus "when" (all-match gating), "one_of" (>=1 non-empty in a group), and
    "owners[].first_name" array-wildcard paths. See problem.md for the exact semantics."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    doc = json.loads(rest)
    out = part1(doc) if part == 1 else part2(doc)
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
