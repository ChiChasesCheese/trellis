"""od06 Query Audit Log -- YOUR implementation. Run pytest against this file with IMPL=starter.

See problem.md for the full contract: names are a flat table-or-column namespace, records are
never deduped, accessed_in_range must use a binary-search-maintained per-name list (not a scan
of all records), and unaccessed_since must only scan a name -> last-access dict (not all records).
"""

from __future__ import annotations

import bisect
import sys


class QueryAuditLog:
    def __init__(self) -> None:
        pass  # TODO: per-name sorted (ts, query_id) lists + a last-access index

    def record_access(
        self, query_id: str, ts: int, tables: set[str], columns: set[str]
    ) -> None:
        """Record one access to every name in tables | columns at time ts. Never dedupes: the
        same query_id/name/ts combination recorded twice yields two entries. ts is not
        guaranteed to arrive non-decreasing -- insert in sorted position, don't just append."""
        raise NotImplementedError  # TODO

    def accessed_in_range(self, name: str, t_start: int, t_end: int) -> list[str]:
        """query_ids that accessed `name` within [t_start, t_end] (inclusive), sorted by
        (ts, query_id); a query_id recorded multiple times in range appears multiple times.
        Never seen -> []. t_start > t_end -> []. Must use binary search, not a linear scan."""
        raise NotImplementedError  # TODO

    def unaccessed_since(self, t: int) -> set[str]:
        """Names that have been accessed at least once, but whose most recent access is
        strictly before t. Names never accessed at all are excluded. Must avoid scanning every
        name's full history on every call."""
        raise NotImplementedError  # TODO


def _parse_csv(field: str) -> set[str]:
    return set() if field == "-" else set(field.split(","))


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh QueryAuditLog from RECORD/RANGE/UNSINCE lines (see problem.md for the line
    format). part1's worked example only uses RECORD/RANGE; part2's also exercises UNSINCE --
    both are driven by this same function since it's one class."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
