"""od12 Top K Book Sales -- YOUR implementation. Run the tests against this file with
IMPL=starter. See problem.md for every rule (cumulative counts, tie-break, the lazy-invalidation
heap efficiency requirement, refund atomicity, and rank())."""

from __future__ import annotations

import sys


class BookSalesTracker:
    def __init__(self) -> None:
        pass  # TODO

    def best_sellers(self, books: list[str], counts: list[int], k: int) -> list[str]:
        raise NotImplementedError  # TODO: cumulative add, then top-k by (total desc, name asc)

    def rank(self, book: str) -> int:
        raise NotImplementedError  # TODO Part3: 1-based rank, KeyError if unknown


def part1(lines: list[str]) -> list[str]:
    # TODO: parse "BEST <k> <n> <book1> <count1> ..." -> space-joined names or "-"
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO: same commands as part1; this is the part exercised for efficiency
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO: adds negative counts (refunds, all-or-nothing -> "ERROR") and "RANK <book>"
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
