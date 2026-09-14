"""q42 Loose-Schema Record Aggregation — YOUR implementation.

RECONSTRUCTED TRAINING PROBLEM (two-hop: 1p3a transcript, self-described as an interviewer
reconstruction) — see problem.md's warning block. Rules/examples below match problem.md; the
precise stdin/stdout framing is this repo's own.

Input shape (see problem.md):
    PART n
    <header line>          "N"  (Part 1, or Part 3 without grouping)
                            "N group_by_key"  (Part 2, or Part 3 with grouping)
    <record line> x N       space-separated key=value tokens, order not guaranteed,
                            last occurrence of a duplicate key wins, unknown keys ignored
                            (except by Part 3's schema, which counts everything)
"""
from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """Header 'N', then N record lines. One '<currency> <total>' line per currency with >=1
    valid record (non-negative-int amount + non-empty currency), sorted by currency."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Header 'N group_by_key', then N record lines. One '<group> <currency> <total>' line per
    (group, currency) with >=1 valid record, sorted by (group, currency); missing group_by_key
    on an otherwise-valid record groups under the literal string '__none__'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Header 'N' or 'N group_by_key' (same totals logic as part1/part2, whichever shape), then
    N record lines. Totals lines, then a literal 'SCHEMA' line, then one '<key> <count>' line per
    key seen anywhere in the input (including unknown keys and keys from invalid records),
    sorted alphabetically -- count = number of records containing that key at least once."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw or not raw[0].strip():
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
