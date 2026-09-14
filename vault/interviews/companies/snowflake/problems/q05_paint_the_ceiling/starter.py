"""q05 Paint the Ceiling — YOUR implementation. Run: python drill.py test q05"""
from __future__ import annotations

import sys


def part1(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    """Generate n sides via sides[1]=s0, sides[i]=((k*sides[i-1]+b) mod m)+1+sides[i-1],
    then count ordered pairs (i,j), repetition allowed, with sides[i]*sides[j] <= a."""
    # TODO
    return 0


def part2(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    """Same semantics as part1, but O(n log n) for n up to 1e6."""
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
    if header[0].upper() == "PART":
        part = int(header[1])
        vals = lines[idx].split()
        idx += 1
    else:
        part = 2
        vals = header
    s0, n, k, b, m, a = (int(x) for x in vals)
    fn = part1 if part == 1 else part2
    stdout.write(f"{fn(s0, n, k, b, m, a)}\n")


if __name__ == "__main__":
    main()
