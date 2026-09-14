"""q36 Time-based KV map — reference solution.

Per key three parallel lists kept sorted by write time (insort, so out-of-order writes work).
get = bisect_right(times, t) - 1: the largest write time <= t. A version with a TTL is alive on
[time, time + ttl) — the end is exclusive.
"""
from __future__ import annotations

import sys
from bisect import bisect_right


class MultiTimeMap:
    def __init__(self) -> None:
        self.times: dict[str, list[int]] = {}
        self.values: dict[str, list] = {}
        self.expires: dict[str, list] = {}   # expiry time (exclusive) or None

    def set(self, key, value, time: int, ttl: int | None = None) -> None:
        ts = self.times.setdefault(key, [])
        vs = self.values.setdefault(key, [])
        ex = self.expires.setdefault(key, [])
        i = bisect_right(ts, time)
        end = None if ttl is None else time + ttl
        if i and ts[i - 1] == time:          # same key + same time: overwrite (last set wins)
            vs[i - 1], ex[i - 1] = value, end
        else:
            ts.insert(i, time)
            vs.insert(i, value)
            ex.insert(i, end)

    def _alive(self, key, i: int, time: int) -> bool:
        end = self.expires[key][i]
        return end is None or time < end     # time == time+ttl is already expired

    def get(self, key, time: int):
        ts = self.times.get(key)
        if not ts:
            return None
        i = bisect_right(ts, time) - 1       # largest write time <= time ('<=', so t == write hits)
        if i < 0 or not self._alive(key, i, time):
            return None                      # expired newest version: no fallback to older ones
        return self.values[key][i]

    def get_all(self, key, time: int) -> list:
        ts = self.times.get(key, [])
        n = bisect_right(ts, time)
        return [self.values[key][i] for i in range(n) if self._alive(key, i, time)]


def first_missing_positive(nums: list[int]) -> int:
    present = set(nums)                      # O(n) time; O(n) extra space (set) is fine here
    i = 1
    while i in present:
        i += 1
    return i


def process(lines: list[str], part: int) -> list[str]:
    if part == 4:
        return [str(first_missing_positive([int(x) for x in (lines[0] if lines else "").split()]))]
    m, out = MultiTimeMap(), []
    for ln in lines:
        cmd, key, *rest = ln.split()
        if cmd == "SET":
            m.set(key, rest[0], int(rest[1]), int(rest[2]) if len(rest) > 2 else None)
        elif cmd == "GET":
            v = m.get(key, int(rest[0]))
            out.append("null" if v is None else str(v))
        elif cmd == "GETALL":
            out.append(" ".join(map(str, m.get_all(key, int(rest[0])))))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines()]
    if not lines or not lines[0]:
        return
    part = int(lines[0].split()[1])
    out = process([ln for ln in lines[1:] if ln] if part != 4 else lines[1:2], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
