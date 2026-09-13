"""q33 Analytical DB min_by_key — YOUR implementation. Run: python drill.py test q33"""
from __future__ import annotations

import json
import sys

Record = dict[str, int]


class RecordComparator:
    def __init__(self, key: str, direction: str) -> None:
        # TODO (direction must be 'asc' or 'desc' -> ValueError otherwise)
        self.key, self.direction = key, direction

    def compare(self, a: Record, b: Record) -> int:
        """-1 if a comes before b, 0 if neither, 1 if a comes after b. Missing key = 0."""
        # TODO
        return 0


Comparator = RecordComparator


def make_comparator(key: str, direction: str):
    return RecordComparator(key, direction).compare


class ChainedComparator:
    def __init__(self, comparators: list[RecordComparator]) -> None:
        self.comparators = comparators

    def compare(self, a: Record, b: Record) -> int:
        # TODO
        return 0


def first_by_key(key: str, direction: str, records: list[Record]) -> Record | None:
    # TODO
    return None


def min_by_key(key: str, records: list[Record]) -> Record | None:
    # TODO
    return None


def sort_by(specs: list[tuple[str, str]], records: list[Record]) -> list[Record]:
    # TODO
    return []


def top_k(specs: list[tuple[str, str]], k: int, records: list[Record]) -> list[Record]:
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """MIN key -> record json | null."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """+ FIRST key asc|desc."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """+ COMPARE key asc|desc (first two records) -> -1 | 0 | 1."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """+ SORT k:dir,... / TOP n k:dir,..."""
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
