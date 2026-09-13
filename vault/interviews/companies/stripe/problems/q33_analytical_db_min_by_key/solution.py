"""q33 Analytical DB min_by_key — reference solution.

Records are dicts of str -> int; a missing key reads as 0.  The comparator is the single source of
ordering: first_by_key keeps `best` and replaces it only when compare(rec, best) == -1 (strict, so
ties keep the earliest record); sort_by uses functools.cmp_to_key on a chained comparator (stable).
"""
from __future__ import annotations

import json
import sys
from functools import cmp_to_key

Record = dict[str, int]


class RecordComparator:
    def __init__(self, key: str, direction: str) -> None:
        if direction not in ("asc", "desc"):
            raise ValueError(f"direction must be 'asc' or 'desc', got {direction!r}")
        self.key = key
        self.sign = 1 if direction == "asc" else -1

    def compare(self, a: Record, b: Record) -> int:
        va, vb = a.get(self.key, 0), b.get(self.key, 0)      # missing key -> 0 (may sit between negatives and positives)
        if va == vb:
            return 0
        return self.sign * (-1 if va < vb else 1)


Comparator = RecordComparator          # the prompt uses both names


def make_comparator(key: str, direction: str):
    """Functional flavour: returns compare(a, b)."""
    return RecordComparator(key, direction).compare


class ChainedComparator:
    def __init__(self, comparators: list[RecordComparator]) -> None:
        self.comparators = comparators

    def compare(self, a: Record, b: Record) -> int:
        for c in self.comparators:
            r = c.compare(a, b)
            if r != 0:
                return r
        return 0


def first_by_key(key: str, direction: str, records: list[Record]) -> Record | None:
    cmp = RecordComparator(key, direction)
    best: Record | None = None
    for rec in records:
        if best is None or cmp.compare(rec, best) == -1:     # strict: ties keep the first record
            best = rec
    return best


def min_by_key(key: str, records: list[Record]) -> Record | None:
    return first_by_key(key, "asc", records)


def sort_by(specs: list[tuple[str, str]], records: list[Record]) -> list[Record]:
    chain = ChainedComparator([RecordComparator(k, d) for k, d in specs])
    return sorted(records, key=cmp_to_key(chain.compare))    # sorted() is stable


def top_k(specs: list[tuple[str, str]], k: int, records: list[Record]) -> list[Record]:
    return sort_by(specs, records)[:max(k, 0)]


# ---- stdin protocol ---------------------------------------------------------------------------
def dumps(rec: Record | None) -> str:
    return json.dumps(rec, sort_keys=True)


def parse_specs(text: str) -> list[tuple[str, str]]:
    specs = []
    for item in text.split(","):
        key, _, direction = item.strip().rpartition(":")
        specs.append((key, direction))
    return specs


def answer(q: list[str], records: list[Record], part: int) -> list[str]:
    cmd = q[0].upper()
    try:
        if cmd == "MIN":
            return [dumps(min_by_key(q[1], records))]
        if cmd == "FIRST" and part >= 2:
            return [dumps(first_by_key(q[1], q[2], records))]
        if cmd == "COMPARE" and part >= 3 and len(records) >= 2:
            return [str(RecordComparator(q[1], q[2]).compare(records[0], records[1]))]
        if cmd == "SORT" and part >= 4:
            return [dumps(r) for r in sort_by(parse_specs(q[1]), records)]
        if cmd == "TOP" and part >= 4:
            return [dumps(r) for r in top_k(parse_specs(q[2]), int(q[1]), records)]
    except ValueError:
        return ["INVALID_DIRECTION"]
    return []


def run(lines: list[str], part: int) -> list[str]:
    records = [json.loads(ln) for ln in lines if ln.startswith("{")]
    out: list[str] = []
    for ln in lines:
        if not ln.startswith("{"):
            out.extend(answer(ln.split(), records, part))
    return out


def part1(lines: list[str]) -> list[str]:
    """MIN key -> record json | null."""
    return run(lines, 1)


def part2(lines: list[str]) -> list[str]:
    """+ FIRST key asc|desc."""
    return run(lines, 2)


def part3(lines: list[str]) -> list[str]:
    """+ COMPARE key asc|desc (first two records) -> -1 | 0 | 1."""
    return run(lines, 3)


def part4(lines: list[str]) -> list[str]:
    """+ SORT k:dir,... / TOP n k:dir,..."""
    return run(lines, 4)


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
