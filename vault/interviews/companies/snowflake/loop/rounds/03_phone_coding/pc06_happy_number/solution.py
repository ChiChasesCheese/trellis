"""pc06 Happy Number -- reference solution.

The map f(n) = sum of squares of digits sends every positive integer into a small range
(any n >= 1000 shrinks: a d-digit number maps to at most 81*d), so iterating f always ends in a
cycle. n is happy iff that cycle is the fixed point 1.

Part1 detects the cycle with a set of seen values: O(cycle + tail) time and memory.
Part2 is the interview follow-up "now do it in O(1) extra space": Floyd's tortoise and hare on
the implicit linked list n -> f(n) -> f(f(n)) ...; they meet inside the cycle, and n is happy iff
they meet at 1. No container grows with the input.
Part3 generalises to base b and exponent p (f(n) = sum of digit^p in base b) and reports the
cycle the sequence falls into: its length and its smallest member, using Floyd plus Brent-style
measurement, still O(1) extra space. (reconstructed follow-up)
"""

from __future__ import annotations

import sys


def _step(n: int, base: int = 10, power: int = 2) -> int:
    total = 0
    while n:
        n, d = divmod(n, base)
        total += d ** power
    return total


def _check(n: int) -> None:
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"n must be a positive integer, got {n!r}")


# --------------------------------------------------------------------------- Part 1
def is_happy_set(n: int) -> bool:
    _check(n)
    seen: set[int] = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = _step(n)
    return n == 1


# --------------------------------------------------------------------------- Part 2
def is_happy_floyd(n: int) -> bool:
    """O(1) extra space."""
    _check(n)
    slow, fast = n, _step(n)
    while fast != 1 and slow != fast:
        slow = _step(slow)
        fast = _step(_step(fast))
    return fast == 1


# --------------------------------------------------------------------------- Part 3
def cycle_info(n: int, base: int = 10, power: int = 2) -> tuple[int, int]:
    """(cycle length, smallest value in the cycle) that iterating f from n falls into.
    Happy numbers in base 10 / power 2 give (1, 1). O(1) extra space."""
    _check(n)
    if base < 2:
        raise ValueError("base must be >= 2")
    if power < 1:
        raise ValueError("power must be >= 1")
    slow, fast = _step(n, base, power), _step(_step(n, base, power), base, power)
    while slow != fast:
        slow = _step(slow, base, power)
        fast = _step(_step(fast, base, power), base, power)
    length, smallest, cur = 1, slow, _step(slow, base, power)
    while cur != slow:
        length += 1
        if cur < smallest:
            smallest = cur
        cur = _step(cur, base, power)
    return length, smallest


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """one positive integer per line -> 'true'/'false' per line."""
    return ["true" if is_happy_set(int(x)) else "false" for x in lines]


def part2(lines: list[str]) -> list[str]:
    return ["true" if is_happy_floyd(int(x)) else "false" for x in lines]


def part3(lines: list[str]) -> list[str]:
    """one line per query: 'n base power' -> 'length smallest'."""
    out = []
    for line in lines:
        n, base, power = map(int, line.split())
        length, smallest = cycle_info(n, base, power)
        out.append(f"{length} {smallest}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
