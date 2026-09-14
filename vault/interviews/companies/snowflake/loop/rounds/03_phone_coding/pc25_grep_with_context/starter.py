"""pc25 Grep With Context Lines -- YOUR implementation. Run the tests against this file with
IMPL=starter.

Like `grep -C N`: matching lines plus N lines of context before/after, overlapping windows
merged, original order, no duplicates.
"""

from __future__ import annotations

import sys
from typing import Iterable, Iterator


def grep(lines: list[str], search_target: str, lines_around: int) -> list[str]:
    """Part1: matching lines plus up to lines_around before/after, merged, deduped, in order.
    ValueError if lines_around < 0."""
    # TODO
    return []


def grep_grouped(lines: list[str], search_target: str, before: int, after: int) -> list[str]:
    """Part2 (reconstructed): asymmetric -B/-A, with a literal '--' line between non-adjacent
    kept runs (never before the first or after the last). ValueError if before/after < 0."""
    # TODO
    return []


def grep_stream(lines: Iterable[str], search_target: str, lines_around: int) -> Iterator[str]:
    """Part3 (reconstructed): `lines` is a one-pass iterator. O(lines_around) auxiliary memory
    (a bounded ring buffer), not O(n). ValueError if lines_around < 0."""
    # TODO
    return iter([])


def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
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
