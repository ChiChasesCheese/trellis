"""pc05 Max Events II -- reference solution.

Part1 is LC 1751: events [start, end, value] with INCLUSIVE end, attend at most k non-overlapping
events (the next event must start strictly after the previous one ends), maximise total value.
Sort by start; dp[j][i] = best value using events i.. with at most j picks;
dp[j][i] = max(dp[j][i+1], value[i] + dp[j-1][nxt[i]]) where nxt[i] is the first event whose start
is strictly greater than end[i] (bisect on the sorted starts). O(n log n + n*k).

Part2 keeps the whole dp table and walks it forward to recover one optimal set of events,
returned as ORIGINAL indices in ascending order. On a tie (skip and take give the same value) we
prefer TAKE, which makes the reconstruction deterministic.

Part3 drops the k limit (the classic weighted interval scheduling, LC 1235 shape) and must scale
to 10^5 events: sort by end; best[i] = max(best[i-1], value[i] + best[p]) with p = number of events
whose end is strictly less than start[i]. O(n log n), O(n) memory.
"""

from __future__ import annotations

import sys
from bisect import bisect_left, bisect_right


# --------------------------------------------------------------------------- shared
def _validate(events: list[list[int]]) -> None:
    for e in events:
        if len(e) != 3:
            raise ValueError(f"event must be [start, end, value], got {e!r}")
        s, t, v = e
        if s > t:
            raise ValueError(f"start {s} is after end {t}")
        if v < 0:
            raise ValueError(f"value must be non-negative, got {v}")


def _table(events: list[list[int]], k: int):
    """Returns (order, nxt, dp) with events sorted by start; dp[j][i] as described above."""
    _validate(events)
    if k < 0:
        raise ValueError("k must be >= 0")
    order = sorted(range(len(events)), key=lambda i: (events[i][0], events[i][1], i))
    starts = [events[i][0] for i in order]
    n = len(order)
    nxt = [bisect_right(starts, events[order[i]][1]) for i in range(n)]
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, k + 1):
        prev, cur = dp[j - 1], dp[j]
        for i in range(n - 1, -1, -1):
            take = events[order[i]][2] + prev[nxt[i]]
            skip = cur[i + 1]
            cur[i] = take if take >= skip else skip
    return order, nxt, dp


# --------------------------------------------------------------------------- Part 1
def max_value(events: list[list[int]], k: int) -> int:
    if not events or k == 0:
        _validate(events)
        return 0
    _, _, dp = _table(events, k)
    return dp[k][0]


# --------------------------------------------------------------------------- Part 2
def max_value_with_events(events: list[list[int]], k: int) -> tuple[int, list[int]]:
    """Best total value and one optimal set of ORIGINAL indices, ascending. Tie -> take."""
    if not events or k == 0:
        _validate(events)
        return 0, []
    order, nxt, dp = _table(events, k)
    chosen: list[int] = []
    i, j, n = 0, k, len(order)
    while i < n and j > 0:
        take = events[order[i]][2] + dp[j - 1][nxt[i]]
        if take >= dp[j][i + 1] and events[order[i]][2] > 0:
            chosen.append(order[i])
            i, j = nxt[i], j - 1
        else:
            i += 1
    return dp[k][0], sorted(chosen)


# --------------------------------------------------------------------------- Part 3
def max_value_unbounded(events: list[list[int]]) -> int:
    """No limit on the number of events. O(n log n)."""
    _validate(events)
    order = sorted(range(len(events)), key=lambda i: (events[i][1], events[i][0], i))
    ends = [events[i][1] for i in order]
    best = [0] * (len(order) + 1)
    for pos, idx in enumerate(order, start=1):
        s, _, v = events[idx]
        p = bisect_left(ends, s)  # events ending strictly before s
        take = v + best[p]
        best[pos] = take if take > best[pos - 1] else best[pos - 1]
    return best[-1]


# --------------------------------------------------------------------------- line-driven wrappers
def _read_events(lines: list[str], idx: int) -> tuple[list[list[int]], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    events = [list(map(int, lines[idx + t].split())) for t in range(int(n))]
    return events, idx + int(n)


def _read_k(line: str) -> int:
    tag, k = line.split()
    if tag != "K":
        raise ValueError(f"expected 'K <k>', got {line!r}")
    return int(k)


def part1(lines: list[str]) -> list[str]:
    """'K <k>' / 'N <n>' / n lines 's e v' -> one line: the best value."""
    k = _read_k(lines[0])
    events, _ = _read_events(lines, 1)
    return [str(max_value(events, k))]


def part2(lines: list[str]) -> list[str]:
    """Same input as part1 -> line 1 best value, line 2 chosen original indices space-separated
    (ascending; '-' when nothing is chosen)."""
    k = _read_k(lines[0])
    events, _ = _read_events(lines, 1)
    best, chosen = max_value_with_events(events, k)
    return [str(best), " ".join(map(str, chosen)) if chosen else "-"]


def part3(lines: list[str]) -> list[str]:
    """'N <n>' / n lines 's e v' -> one line: the best value with no limit on the count."""
    events, _ = _read_events(lines, 0)
    return [str(max_value_unbounded(events))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
