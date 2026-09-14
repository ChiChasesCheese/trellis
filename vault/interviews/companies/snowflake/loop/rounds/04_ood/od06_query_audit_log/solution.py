"""od06 Query Audit Log -- reference solution.

Each name (table or column) keeps its own list of (ts, query_id) pairs, always kept sorted by
`bisect.insort` -- accesses can arrive out of ts order, so `record_access` must find its sorted
insertion point rather than assume append-at-end. `accessed_in_range` locates the [t_start,
t_end] slice with two bisects (using (t, "") / (t_end + 1, "") as boundary keys -- the empty
string sorts before any real, non-empty query_id, so it acts as an exact "ts >= X" cursor without
needing a string upper-bound sentinel) instead of scanning the whole list, so its cost is
O(log(that name's record count) + hits), never proportional to the total record count.

`unaccessed_since` only needs a single dict of `name -> most-recent ts`, updated in O(1) per
`record_access` call; the query itself is one pass over that dict (size = distinct name count,
not total record count) -- see problem.md's "并发追问" #3 for why a fancier
sorted-by-last-access structure is a real but non-trivial follow-up (a naive "insert-only, lazily
invalidate" sorted list degrades badly when almost every access refreshes the max, which is
exactly the on-the-record scenario this solution avoids by not building it in the first place).
"""

from __future__ import annotations

import bisect
import sys


class QueryAuditLog:
    def __init__(self) -> None:
        self._records: dict[str, list[tuple[int, str]]] = {}
        self._last_access: dict[str, int] = {}

    def record_access(
        self, query_id: str, ts: int, tables: set[str], columns: set[str]
    ) -> None:
        for name in tables | columns:
            bisect.insort(self._records.setdefault(name, []), (ts, query_id))
            if ts > self._last_access.get(name, float("-inf")):
                self._last_access[name] = ts

    def accessed_in_range(self, name: str, t_start: int, t_end: int) -> list[str]:
        if t_start > t_end:
            return []
        lst = self._records.get(name)
        if not lst:
            return []
        lo = bisect.bisect_left(lst, (t_start, ""))
        hi = bisect.bisect_left(lst, (t_end + 1, ""))
        return [query_id for _, query_id in lst[lo:hi]]

    def unaccessed_since(self, t: int) -> set[str]:
        return {name for name, ts in self._last_access.items() if ts < t}


# ---------------------------------------------------------------------- line-driven wrappers
def _parse_csv(field: str) -> set[str]:
    return set() if field == "-" else set(field.split(","))


def _run(lines: list[str]) -> list[str]:
    log = QueryAuditLog()
    out: list[str] = []
    for raw in lines:
        fields = raw.split()
        verb = fields[0]
        if verb == "RECORD":
            query_id, ts = fields[1], int(fields[2])
            tables = _parse_csv(fields[3])
            columns = _parse_csv(fields[4])
            log.record_access(query_id, ts, tables, columns)
        elif verb == "RANGE":
            name, t_start, t_end = fields[1], int(fields[2]), int(fields[3])
            out.append(repr(log.accessed_in_range(name, t_start, t_end)))
        elif verb == "UNSINCE":
            out.append(repr(sorted(log.unaccessed_since(int(fields[1])))))
        else:
            raise ValueError(f"bad line: {raw!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _run(lines)


def part2(lines: list[str]) -> list[str]:
    return _run(lines)


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
