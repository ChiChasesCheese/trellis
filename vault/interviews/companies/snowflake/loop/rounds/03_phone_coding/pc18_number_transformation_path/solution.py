"""pc18 Number Transformation Path -- reference solution.

Ops (reconstructed, since the preview names them but not their exact domain -- see
problem.md's "规则" for the declared choice): from a positive integer n you may move to
  - add:   n + 2               (always legal)
  - sub:   n - 2                (legal only while the result stays >= 1)
  - split: n // 2, but ONLY when n is even (an odd n cannot be split -- this is the domain
    restriction the "parity" hint in the task description is pointing at)
`add`/`sub` never change parity. `split` is the only move that can, and it is only available
from an even number. Consequence: starting from an ODD a, you can never touch an even number at
all (you would need a split to leave the odd class, and split needs an even input) -- so an odd
a can only ever reach odd targets. Starting from an EVEN a, everything is reachable: to hit any
target b you can walk (via add/sub, staying even) to the even number 2*b and then split once to
land exactly on b (if b is itself even you don't even need the split -- a direct add/sub walk
already works since both endpoints are even).

Part1 returns any valid path (not necessarily shortest) built by that direct construction.
Part2 (reconstructed) finds a SHORTEST path with a bounded BFS: no state of the search ever
needs to exceed 2*max(a, b) + 4, because the direct Part1 construction already achieves the
target by walking to at most 2*b (or b itself) before splitting, so the optimum cannot need to
wander further than that plus a small margin for the sub direction.
"""

from __future__ import annotations

import sys
from collections import deque


def _check(a: int, b: int) -> None:
    if not isinstance(a, int) or not isinstance(b, int) or a < 1 or b < 1:
        raise ValueError(f"a and b must be positive integers, got a={a!r} b={b!r}")


# --------------------------------------------------------------------------- Part 1
def transform(a: int, b: int) -> list[int] | None:
    """Any valid sequence of positive integers from a to b inclusive (not necessarily shortest),
    or None if b is unreachable from a (odd a, even b)."""
    _check(a, b)
    if a == b:
        return [a]
    if a % 2 == 1 and b % 2 == 0:
        return None

    def walk(path: list[int], start: int, target: int) -> None:
        step = 2 if target > start else -2
        cur = start
        while cur != target:
            cur += step
            path.append(cur)

    path = [a]
    if a % 2 == b % 2:
        walk(path, a, b)
    else:
        # a even, b odd: walk (staying even) to 2*b, then one split lands exactly on b.
        m = 2 * b
        walk(path, a, m)
        path.append(b)
    return path


# --------------------------------------------------------------------------- Part 2
def shortest_transform(a: int, b: int) -> list[int] | None:
    """Shortest sequence of positive integers from a to b, via bounded BFS. None if unreachable
    (same odd-a/even-b rule as transform)."""
    _check(a, b)
    if a == b:
        return [a]
    if a % 2 == 1 and b % 2 == 0:
        return None

    bound = 2 * max(a, b) + 4
    prev: dict[int, int | None] = {a: None}
    queue: deque[int] = deque([a])
    while queue:
        cur = queue.popleft()
        if cur == b:
            break
        neighbors = []
        if cur + 2 <= bound:
            neighbors.append(cur + 2)
        if cur - 2 >= 1:
            neighbors.append(cur - 2)
        if cur % 2 == 0 and cur // 2 >= 1:
            neighbors.append(cur // 2)
        for nxt in neighbors:
            if nxt not in prev:
                prev[nxt] = cur
                queue.append(nxt)

    if b not in prev:
        return None  # not expected to trigger given the reachability rule + bound above
    path = []
    cur: int | None = b
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


# --------------------------------------------------------------------------- line-driven wrappers
def _format(path: list[int] | None) -> str:
    return "IMPOSSIBLE" if path is None else " ".join(map(str, path))


def part1(lines: list[str]) -> list[str]:
    """each line: 'a b' -> the path (space-separated) or 'IMPOSSIBLE'."""
    out = []
    for line in lines:
        a, b = map(int, line.split())
        out.append(_format(transform(a, b)))
    return out


def part2(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        a, b = map(int, line.split())
        out.append(_format(shortest_transform(a, b)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
