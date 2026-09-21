"""pc01 Grouped Aggregation -- YOUR implementation. Run the tests against this file with
IMPL=starter.

Rows are CSV lines with no header. Part1/Part2: 'id,amount'. Part3: 'id,category,amount'.
Money must be handled with decimal.Decimal (or integer cents) -- never accumulate with float.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from typing import Iterable, Sequence


def group_sum_streaming(lines: Iterable[str]) -> dict[str, Decimal]:
    """Part1: one pass, dict accumulation via the csv module. ValueError on a malformed row,
    an empty id, or an amount that doesn't parse as a decimal."""
    # TODO
    return {}


def chunked_group_sum(lines: Sequence[str], chunk_size: int, workers: int = 1) -> dict[str, Decimal]:
    """Part2: split into chunk_size-row chunks, aggregate each chunk, merge the partial dicts.
    Must return the same result regardless of chunk_size or workers. ValueError if chunk_size <= 0
    or workers <= 0."""
    # TODO
    return {}


def multi_key_aggregate(lines: Iterable[str]) -> dict[tuple[str, str], dict[str, object]]:
    """Part3: rows 'id,category,amount' -> group by (id, category); sum/count/max per group."""
    # TODO
    return {}


def part1(lines: list[str]) -> list[str]:
    """'id,amount' rows -> 'id,total' lines, sorted by id, amount formatted to 2 decimals."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'CHUNK_SIZE <n>', then 'id,amount' rows -> same output shape as part1."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'id,category,amount' rows -> 'id,category,sum,count,max' lines, sorted by (id, category)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
