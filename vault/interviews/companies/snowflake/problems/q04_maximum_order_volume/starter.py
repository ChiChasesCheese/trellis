"""q04 Maximum Order Volume — YOUR implementation. Run: python drill.py test q04"""
from __future__ import annotations

import sys


def part1(start: list[int], duration: list[int], volume: list[int]) -> int:
    """Correct DP, any complexity. Select non-overlapping calls (call i occupies
    [start[i], start[i]+duration[i])) maximizing sum of volume[i]."""
    # TODO
    return 0


def part2(start: list[int], duration: list[int], volume: list[int]) -> int:
    """Same semantics as part1, but O(n log n) for n up to 1e5."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    if not lines:
        stdout.write("0\n")
        return
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header[0].upper() == "PART" else 2
    n = int(lines[idx])
    idx += 1
    start: list[int] = []
    duration: list[int] = []
    volume: list[int] = []
    for _ in range(n):
        s, d, v = lines[idx].split()
        idx += 1
        start.append(int(s))
        duration.append(int(d))
        volume.append(int(v))
    fn = part1 if part == 1 else part2
    stdout.write(f"{fn(start, duration, volume)}\n")


if __name__ == "__main__":
    main()
