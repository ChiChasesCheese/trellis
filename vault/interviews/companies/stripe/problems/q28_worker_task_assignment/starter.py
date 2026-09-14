"""q28 Worker Task Assignment — YOUR implementation. Run: python drill.py test q28"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """WORKERS/TASKS sections. Least load, ties by id; skills/capacity ignored.
    Return ['task -> worker', ...] in task order then ['worker load', ...] sorted by worker id."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """+ worker must have required_skill; else 'task -> UNASSIGNED'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """+ equal load -> fewer skills first, then id."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """+ capacity: only workers with load + cost <= capacity."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
