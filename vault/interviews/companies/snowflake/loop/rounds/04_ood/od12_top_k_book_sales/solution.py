"""od12 Top K Book Sales -- reference solution.

Source (MED, TrueInterview via kevin-2023-code/Tech-Interview-Questions "Top K Book Sales", LLD,
reported 2026-02): the confirmed shape is "BookSalesTracker() with best_sellers(books, counts, k)
that adds counts cumulatively then returns the top k by total". This is the same mechanics as
LeetCode 1244 "Design A Leaderboard" (addScore cumulative, top(K)) with book names instead of a
sum -- everything about efficiency, refunds, and rank() below is reconstructed.

Part1: correctness only -- best_sellers adds counts cumulatively into a running per-book total,
then returns the top k books by (total desc, name asc), ties on total broken alphabetically.
Part2 (reconstructed): the SAME class must stay efficient across many calls -- no third-party
libs, so this uses a max-heap of (-total, name) entries with LAZY INVALIDATION: every update
pushes a fresh entry without removing the old one for that book; a query pops entries off the
heap, discards ones that no longer match the book's current total (stale), and pushes back every
entry it validated so future queries don't re-pay that cost. Each entry is pushed exactly once
per update and popped-and-validated at most once before either landing in a result or being
discarded forever, so total heap work across N updates and Q queries is O((N + Q*k) log N).
Part3 (reconstructed): best_sellers also accepts negative counts (refunds); a call is rejected
IN FULL (ValueError, no partial effect) if ANY book in the batch would drop below zero total.
rank(book) returns the 1-based rank of a known book under the same ordering, or raises KeyError.
"""

from __future__ import annotations

import heapq
import sys


class BookSalesTracker:
    def __init__(self) -> None:
        self._totals: dict[str, int] = {}
        # max-heap via negated totals: (-total, name). May contain STALE entries left behind by
        # earlier updates to the same book; validity is checked against self._totals at pop time.
        self._heap: list[tuple[int, str]] = []

    def best_sellers(self, books: list[str], counts: list[int], k: int) -> list[str]:
        """Add counts[i] to books[i]'s running total (for every i), THEN return the top k books
        by (total desc, name asc). Part3 rule: if any resulting total would go negative, the
        WHOLE call is rejected (ValueError) and nothing is applied -- pre-validated before any
        mutation so a rejected refund batch never partially lands."""
        if len(books) != len(counts):
            raise ValueError("books and counts must be the same length")

        # pre-validate (Part3): compute the deltas per book first, reject the whole batch if any
        # resulting total would go negative -- Part1/2 callers only ever pass non-negative counts
        # so this check is a no-op for them.
        deltas: dict[str, int] = {}
        for name, delta in zip(books, counts):
            deltas[name] = deltas.get(name, 0) + delta
        for name, delta in deltas.items():
            prospective = self._totals.get(name, 0) + delta
            if prospective < 0:
                raise ValueError(f"refund would take {name!r} below zero")

        for name, delta in deltas.items():
            new_total = self._totals.get(name, 0) + delta
            self._totals[name] = new_total
            heapq.heappush(self._heap, (-new_total, name))

        return self._top_k(k)

    def rank(self, book: str) -> int:
        """1-based rank under the same (total desc, name asc) ordering as best_sellers. Raises
        KeyError for a book that has never appeared in any best_sellers call. O(n log n) -- simple
        and obviously correct; the heap is not reused here since rank() is not the hot path this
        problem's efficiency requirement (Part2) targets."""
        if book not in self._totals:
            raise KeyError(book)
        ordered = sorted(self._totals.items(), key=lambda item: (-item[1], item[0]))
        for i, (name, _total) in enumerate(ordered):
            if name == book:
                return i + 1
        raise AssertionError("unreachable: book was in self._totals")

    def _top_k(self, k: int) -> list[str]:
        if k <= 0:
            return []
        result: list[str] = []
        popped: list[tuple[int, str]] = []
        seen: set[str] = set()
        while self._heap and len(result) < k:
            entry = heapq.heappop(self._heap)
            neg_total, name = entry
            if name in seen:
                continue  # a newer valid entry for this name was already used/queued
            if self._totals.get(name) != -neg_total:
                continue  # stale: discard permanently, do not push back
            popped.append(entry)
            seen.add(name)
            result.append(name)
        for entry in popped:
            heapq.heappush(self._heap, entry)
        return result


# --------------------------------------------------------------------------- command stream
def _run(lines: list[str], allow_refunds: bool) -> list[str]:
    tracker = BookSalesTracker()
    out: list[str] = []
    for line in lines:
        fields = line.split()
        cmd = fields[0]
        if cmd == "BEST":
            k = int(fields[1])
            n = int(fields[2])
            rest = fields[3:]
            books = rest[0::2][:n]
            counts = [int(c) for c in rest[1::2][:n]]
            try:
                names = tracker.best_sellers(books, counts, k)
            except ValueError:
                out.append("ERROR")
            else:
                out.append(" ".join(names) if names else "-")
        elif cmd == "RANK":
            try:
                out.append(str(tracker.rank(fields[1])))
            except KeyError:
                out.append("-")
        else:
            raise ValueError(f"unknown command: {line!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _run(lines, allow_refunds=False)


def part2(lines: list[str]) -> list[str]:
    return _run(lines, allow_refunds=False)


def part3(lines: list[str]) -> list[str]:
    return _run(lines, allow_refunds=True)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
