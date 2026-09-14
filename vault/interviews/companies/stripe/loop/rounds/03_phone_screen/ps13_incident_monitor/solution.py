"""ps13 Incident Monitor — reference solution.

Part 1's rule (single global (window, threshold), sorted input) has real candidate-report
provenance -- see problem.md's warning block. Parts 2-4 are this suite's own design, built as
successive generalizations of the same rolling-window-per-key engine:
  Part 2 = Part 1's rule, just without assuming pre-sorted input (this implementation always
           sorts by (timestamp, input order) first, so Part 1 IS Part 2 -- the split exists
           because Part 1's real-world rule explicitly promises sorted input and Part 2's does
           not, not because the code differs).
  Part 3 = Part 1's rule with a per-merchant (window, threshold) override table.
  Part 4 = a three-level (0/1/2) generalization of Part 1's two-state (below/above) machine,
           emitting one event per threshold boundary crossed (handles multi-level jumps).

Every level/state machine is per (merchant_id, status_code) key -- keys never share a deque or a
running sum (the classic S04 bug this problem's tests target).
"""

from __future__ import annotations

import sys
from collections import defaultdict, deque
from typing import Callable, NamedTuple

PairKey = tuple[str, str]  # (merchant_id, status_code)

# Part 4's ladder: event emitted when arriving AT a given level, per direction of travel.
LEVEL_UP_EVENT = {1: "TRIGGER", 2: "ESCALATE"}  # arriving at level 1 / 2 from below
LEVEL_DOWN_EVENT = {1: "DEESCALATE", 0: "RESOLVE"}  # arriving at level 1 / 0 from above


class Record(NamedTuple):
    ts: int
    merchant: str
    status: str
    count: int
    order: int  # input position (post blank-line filtering) -- tie-break for equal timestamps


# ------------------------------------------------------------------ parsing
def _parse_params(line: str) -> dict[str, int]:
    """'WINDOW=3 THRESHOLD=4' -> {'WINDOW': 3, 'THRESHOLD': 4}."""
    return {k: int(v) for k, _, v in (tok.partition("=") for tok in line.split())}


def _parse_records(lines: list[str]) -> list[Record]:
    """'timestamp,merchant_id,status_code,count' lines -> Records, tagged with input position."""
    out: list[Record] = []
    for i, raw in enumerate(lines):
        ts, merchant, status, count = (p.strip() for p in raw.split(","))
        out.append(Record(int(ts), merchant, status, int(count), i))
    return out


def _parse_and_sort(lines: list[str]) -> list[Record]:
    """Parse then stable-sort by (timestamp, input order). A no-op reorder when the input is
    already sorted (Part 1's guarantee), which is exactly why part1 and part2 can share this."""
    return sorted(_parse_records(lines), key=lambda r: (r.ts, r.order))


# ------------------------------------------------------------------ core engines
def _events_single_threshold(records: list[Record], rule_for: Callable[[str], tuple[int, int]]) -> list[str]:
    """One TRIGGER/RESOLVE state machine per (merchant_id, status_code) key. `rule_for(merchant)`
    returns that merchant's fixed (window, threshold); records MUST already be in the order they
    should be processed in (timestamp, then input order)."""
    windows: dict[PairKey, deque[tuple[int, int]]] = defaultdict(deque)  # key -> deque[(ts,count)]
    sums: dict[PairKey, int] = defaultdict(int)
    triggered: dict[PairKey, bool] = defaultdict(bool)
    events: list[str] = []
    for r in records:
        key = (r.merchant, r.status)
        window, threshold = rule_for(r.merchant)
        dq = windows[key]
        dq.append((r.ts, r.count))
        sums[key] += r.count
        while dq[0][0] < r.ts - window + 1:  # evict volume that fell out of the closed window
            _, expired_count = dq.popleft()
            sums[key] -= expired_count
        now_above = sums[key] >= threshold
        if now_above and not triggered[key]:
            events.append(f"{r.ts},{r.merchant},{r.status},TRIGGER")
            triggered[key] = True
        elif not now_above and triggered[key]:
            events.append(f"{r.ts},{r.merchant},{r.status},RESOLVE")
            triggered[key] = False
    return events


def _level(total: int, warn: int, crit: int) -> int:
    """0 (< warn) / 1 (warn <= total < crit) / 2 (>= crit) -- both boundaries non-strict upward."""
    if total >= crit:
        return 2
    if total >= warn:
        return 1
    return 0


def _events_two_level(records: list[Record], warn: int, crit: int, window: int) -> list[str]:
    """Part 4's three-level ladder. A record can move a pair more than one level in a single step
    (e.g. a huge count, or the window sliding forward past a lot of old volume) -- emit one event
    per boundary crossed, in traversal order, all at that record's timestamp."""
    windows: dict[PairKey, deque[tuple[int, int]]] = defaultdict(deque)
    sums: dict[PairKey, int] = defaultdict(int)
    levels: dict[PairKey, int] = defaultdict(int)
    events: list[str] = []
    for r in records:
        key = (r.merchant, r.status)
        dq = windows[key]
        dq.append((r.ts, r.count))
        sums[key] += r.count
        while dq[0][0] < r.ts - window + 1:
            _, expired_count = dq.popleft()
            sums[key] -= expired_count
        old_level, new_level = levels[key], _level(sums[key], warn, crit)
        if new_level > old_level:
            for lvl in range(old_level + 1, new_level + 1):
                events.append(f"{r.ts},{r.merchant},{r.status},{LEVEL_UP_EVENT[lvl]}")
        elif new_level < old_level:
            for lvl in range(old_level - 1, new_level - 1, -1):
                events.append(f"{r.ts},{r.merchant},{r.status},{LEVEL_DOWN_EVENT[lvl]}")
        levels[key] = new_level
    return events


# ------------------------------------------------------------------ parts
def part1(lines: list[str]) -> list[str]:
    """Single global (WINDOW, THRESHOLD); input already sorted by timestamp."""
    params = _parse_params(lines[0])
    rule = (params["WINDOW"], params["THRESHOLD"])
    records = _parse_and_sort(lines[1:])  # sorting is a no-op on already-sorted input
    return _events_single_threshold(records, lambda _merchant: rule)


def part2(lines: list[str]) -> list[str]:
    """Same rule as part1; log lines may arrive out of order (handled by part1's internal sort)."""
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    """Per-merchant (window, threshold) override table, falling back to a default rule."""
    params = _parse_params(lines[0])
    default_rule = (params["DEFAULT_WINDOW"], params["DEFAULT_THRESHOLD"])
    k = params["RULES"]
    rule_lines, log_lines = lines[1 : 1 + k], lines[1 + k :]
    rules: dict[str, tuple[int, int]] = {}
    for raw in rule_lines:
        merchant, window, threshold = (p.strip() for p in raw.split(","))
        rules[merchant] = (int(window), int(threshold))
    records = _parse_and_sort(log_lines)
    return _events_single_threshold(records, lambda merchant: rules.get(merchant, default_rule))


def part4(lines: list[str]) -> list[str]:
    """Two-severity-level (WARN, CRIT) escalation ladder over the same rolling window."""
    params = _parse_params(lines[0])
    records = _parse_and_sort(lines[1:])
    return _events_two_level(records, params["WARN"], params["CRIT"], params["WINDOW"])


# ------------------------------------------------------------------ I/O
PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3, "PART 4": part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not raw:
        return
    header, body = raw[0], raw[1:]
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    out = PARTS[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
