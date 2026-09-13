"""q36 Time-based KV map — YOUR implementation. Run: python drill.py test q36

Part 1 set/get (latest write time <= t) -> Part 2 get_all -> Part 3 TTL -> Part 4 first_missing_positive.
"""
from __future__ import annotations

import sys
from bisect import bisect_right


class MultiTimeMap:
    def __init__(self) -> None:
        self.times: dict[str, list[int]] = {}      # key -> sorted write times
        self.values: dict[str, list] = {}          # key -> values, parallel to times
        self.expires: dict[str, list] = {}         # key -> time + ttl (or None), parallel

    def set(self, key, value, time: int, ttl: int | None = None) -> None:
        # TODO (same key + same time overwrites)
        pass

    def get(self, key, time: int):
        # TODO
        return None

    def get_all(self, key, time: int) -> list:
        # TODO
        return []


def first_missing_positive(nums: list[int]) -> int:
    # TODO
    return 0


def process(lines: list[str], part: int) -> list[str]:
    # TODO: SET/GET/GETALL commands for parts 1-3; part 4: one line of ints
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines()]
    if not lines or not lines[0]:
        return
    part = int(lines[0].split()[1])
    out = process([ln for ln in lines[1:] if ln] if part != 4 else lines[1:2], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
