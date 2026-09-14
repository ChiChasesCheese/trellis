"""q20 Sequential String -- reference solution.

s is a string of digits that can only be read left to right (like a tape). For each query
string, find the minimum prefix length of s whose MULTISET of digits contains enough of every
digit to assemble some permutation of the query -- or -1 if even the whole tape can't.

The source's own reference solution is WRONG: it matches digits of the query IN ORDER against s
(a subsequence check) instead of comparing digit multisets. Order does not matter for "does this
prefix contain a permutation of the query" -- only counts matter. See problem.md for the concrete
counter-example ("21" vs query "12").

Part1: per digit, binary search a prefix-count table (10 columns x (n+1) rows) for the first
prefix whose count of that digit reaches what's needed; answer is the max over digits.
Part2 (reconstructed): precompute, per digit, the sorted list of positions where it occurs; the
answer for a digit is then a direct index (occ[d][need_d - 1]) with no search at all, so
answering every query costs O(total query length) after an O(n) precompute -- no log factor.
"""

from __future__ import annotations

import bisect
import sys
from collections import Counter


def _validate(s: str, queries: list[str]) -> None:
    if any(not c.isdigit() for c in s):
        raise ValueError("s must contain only digits 0-9")
    for q in queries:
        if any(not c.isdigit() for c in q):
            raise ValueError(f"query must contain only digits 0-9: {q!r}")


# --------------------------------------------------------------------------- Part 1
def sequential_prefix_lengths_binary(s: str, queries: list[str]) -> list[int]:
    """For each query, the minimum prefix length of s that contains a permutation of it, via
    binary search over a per-digit prefix-count table. O(10n) precompute + O(len(q) log n) per
    query."""
    _validate(s, queries)
    n = len(s)
    # counts[d] is the prefix-count column for digit d: counts[d][i] = #occurrences of d in s[:i]
    counts = [[0] * (n + 1) for _ in range(10)]
    for i, ch in enumerate(s):
        d = int(ch)
        for dd in range(10):
            counts[dd][i + 1] = counts[dd][i]
        counts[d][i + 1] += 1

    out: list[int] = []
    for q in queries:
        need = Counter(int(c) for c in q)
        if not need:
            out.append(0)
            continue
        best = 0
        possible = True
        for d, cnt in need.items():
            col = counts[d]
            idx = bisect.bisect_left(col, cnt)
            if idx > n:  # never reaches cnt occurrences
                possible = False
                break
            best = max(best, idx)
        out.append(best if possible else -1)
    return out


# --------------------------------------------------------------------------- Part 2
def sequential_prefix_lengths_fast(s: str, queries: list[str]) -> list[int]:
    """Same answer, O(n) precompute (occurrence-position lists) + O(total query length) total."""
    _validate(s, queries)
    occ: list[list[int]] = [[] for _ in range(10)]
    for i, ch in enumerate(s):
        occ[int(ch)].append(i)

    out: list[int] = []
    for q in queries:
        need = Counter(int(c) for c in q)
        if not need:
            out.append(0)
            continue
        best = -1
        possible = True
        for d, cnt in need.items():
            positions = occ[d]
            if len(positions) < cnt:
                possible = False
                break
            best = max(best, positions[cnt - 1] + 1)
        out.append(best if possible else -1)
    return out


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[str, list[str]]:
    s = lines[0].strip() if lines else ""
    m = int(lines[1]) if len(lines) > 1 else 0
    queries = [lines[2 + i].strip() for i in range(m)]
    return s, queries


def part1(lines: list[str]) -> list[str]:
    """'s' / 'm' / m queries -> m answers (binary search over prefix counts)."""
    s, queries = _read(lines)
    return [str(x) for x in sequential_prefix_lengths_binary(s, queries)]


def part2(lines: list[str]) -> list[str]:
    """same input -> m answers (occurrence-position lists, O(total length))."""
    s, queries = _read(lines)
    return [str(x) for x in sequential_prefix_lengths_fast(s, queries)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    lines = [ln for ln in raw if ln.strip() != "" or True]  # keep structure; s could be ""
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
