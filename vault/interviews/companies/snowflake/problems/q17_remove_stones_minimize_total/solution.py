"""q17 Remove Stones to Minimize the Total -- reference solution.

Part 1 is LC 1962 "Remove Stones to Minimize the Total" verbatim: given `piles`
(each a positive stone count) and `k` operations, each operation picks the pile
with the MOST stones and removes floor(pile / 2) stones from it. After exactly k
operations, return the minimum possible sum (it's also the ONLY possible sum --
always removing from the current maximum is the unique optimal greedy, proven by
an exchange argument: removing from a smaller pile first can never do better than
removing from the largest, since halving a bigger pile always removes at least as
many stones and leaves it no smaller than any pile you could have chosen instead).

Standard solution: max-heap (Python only has a min-heap, so store negatives), pop
the largest k times, replace each popped pile p with p - p//2, push it back, sum
what remains. O(n + k log n).

Part 2 (reconstructed): piles arrive online between operations -- `add(pile)`
inserts a new pile, `apply(k)` immediately runs k halving-operations against
whatever piles exist so far and returns the running total. This is the natural
online counterpart: the same max-heap, just kept alive across calls instead of
rebuilt once.
"""
from __future__ import annotations

import heapq
import sys


def _validate_piles(piles: list[int]) -> None:
    for p in piles:
        if not isinstance(p, int) or isinstance(p, bool) or p < 1:
            raise ValueError(f"pile must be a positive int: {p!r}")


def _validate_k(k: int) -> None:
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError(f"k must be a non-negative int: {k!r}")


# --------------------------------------------------------------------------- Part 1
def min_total_after_k_removals(piles: list[int], k: int) -> int:
    """LC1962: after k operations (halve the current max pile, floor division,
    each time), return the minimum possible total."""
    _validate_piles(piles)
    _validate_k(k)
    heap = [-p for p in piles]
    heapq.heapify(heap)
    for _ in range(k):
        if not heap or heap[0] == 0:
            break  # every pile is already 0; further operations change nothing
        top = -heapq.heappop(heap)
        heapq.heappush(heap, -(top - top // 2))
    return -sum(heap)


# --------------------------------------------------------------------------- Part 2
class StoneStream:
    """Piles arrive online (`add`); `apply(k)` runs k halving-operations against
    everything seen so far and returns the current total. The max-heap and a
    running total are kept alive across calls."""

    def __init__(self) -> None:
        self._heap: list[int] = []
        self._total = 0

    def add(self, pile: int) -> None:
        if not isinstance(pile, int) or isinstance(pile, bool) or pile < 1:
            raise ValueError(f"pile must be a positive int: {pile!r}")
        heapq.heappush(self._heap, -pile)
        self._total += pile

    def apply(self, k: int) -> int:
        _validate_k(k)
        for _ in range(k):
            if not self._heap or self._heap[0] == 0:
                break
            top = -heapq.heappop(self._heap)
            reduction = top // 2
            self._total -= reduction
            heapq.heappush(self._heap, -(top - reduction))
        return self._total


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """'n k' / n piles -> [total]."""
    n, k = map(int, lines[0].split())
    piles = list(map(int, lines[1].split())) if n else []
    return [str(min_total_after_k_removals(piles, k))]


def part2(lines: list[str]) -> list[str]:
    """'m' / m lines 'ADD pile' or 'APPLY k' -> one output line per APPLY."""
    m = int(lines[0])
    stream = StoneStream()
    out: list[str] = []
    for ln in lines[1 : 1 + m]:
        parts = ln.split()
        if parts[0] == "ADD":
            stream.add(int(parts[1]))
        elif parts[0] == "APPLY":
            out.append(str(stream.apply(int(parts[1]))))
        else:
            raise ValueError(f"unknown op: {ln!r}")
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
