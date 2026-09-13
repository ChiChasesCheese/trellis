"""q05 Paint the Ceiling — reference solution.

Generate n "side lengths" via a linear-congruential-style recurrence, then count
ordered pairs (i, j) -- repetition allowed, i.e. i == j is a valid pair -- ranging
over the whole 1..n index range such that sides[i] * sides[j] <= a.

Generation (1-indexed conceptually; 0-indexed list in code):
    sides[1] = s0
    sides[i] = ((k * sides[i-1] + b) mod m) + 1 + sides[i-1]   for i = 2..n

We assume s0 >= 1 (side lengths are physical, per the problem domain). Given
that assumption, every generated side is >= 1: sides[i] = (mod term, which is
in [0, m-1]) + 1 + sides[i-1] >= 1 + sides[i-1] >= 1, so sides only ever grow
(each new side is strictly greater than the previous one by at least 1). This
means sides can never be 0, which lets part2 divide by each side safely.

part1 is the direct O(n^2) brute-force count (fine for the modest n used in
correctness tests). part2 sorts the sides and, for each side x, uses
bisect_right to count how many sides y (over the whole multiset) satisfy
y <= a // x -- since all values are positive integers, x*y <= a is exactly
y <= floor(a / x) = a // x. That is O(n log n) total, well within budget for
n up to ~1e6.
"""
from __future__ import annotations

import sys
from bisect import bisect_right


def _generate(s0: int, n: int, k: int, b: int, m: int) -> list[int]:
    if n <= 0:
        return []
    sides = [s0]
    for _ in range(n - 1):
        prev = sides[-1]
        sides.append(((k * prev + b) % m) + 1 + prev)
    return sides


def part1(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    """Brute-force O(n^2): generate then count every ordered pair directly."""
    sides = _generate(s0, n, k, b, m)
    count = 0
    for x in sides:
        for y in sides:
            if x * y <= a:
                count += 1
    return count


def part2(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    """O(n log n): generate, sort, then bisect per element."""
    sides = _generate(s0, n, k, b, m)
    sorted_sides = sorted(sides)
    total = 0
    for x in sorted_sides:
        if x == 0:
            # Not reachable when s0 >= 1 (see module docstring), but guard the
            # division defensively: 0 * anything <= a whenever a >= 0.
            total += len(sorted_sides) if a >= 0 else 0
            continue
        threshold = a // x
        total += bisect_right(sorted_sides, threshold)
    return total


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
