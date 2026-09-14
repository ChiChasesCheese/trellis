"""qA10 LC 161 One Edit Distance — reference solution.

Part 1 scans to the first mismatch and compares the tails. Part 2 adds the adjacent transposition.
Part 3 reuses the same scan and names the edit. Part 4 is Levenshtein <= k with a band of width 2k+1
around the diagonal (O(k*n) time, O(k) memory) — the full table is 10^8 cells at LC max.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Edit(NamedTuple):
    kind: str    # "insert" | "delete" | "replace" | "swap"
    index: int   # position in s
    char: str    # inserted / replacement char; "" for delete and swap


def _first_mismatch(s: str, t: str) -> int:
    """Index of the first differing character, or min(len) when one is a prefix of the other."""
    n = min(len(s), len(t))
    i = 0
    while i < n and s[i] == t[i]:
        i += 1
    return i


def find_edit(s: str, t: str) -> Edit | None:
    """Part 3: the edit (index = first mismatch) turning s into t, swap allowed; None if not one edit."""
    if abs(len(s) - len(t)) > 1:
        return None
    i = _first_mismatch(s, t)
    if len(s) == len(t):
        if i == len(s):
            return None  # identical: zero edits is not one edit
        if s[i + 1:] == t[i + 1:]:
            return Edit("replace", i, t[i])
        # transposition: positions i, i+1 crossed, rest equal (s[i] != t[i] here, so the chars differ)
        if i + 1 < len(s) and s[i] == t[i + 1] and s[i + 1] == t[i] and s[i + 2:] == t[i + 2:]:
            return Edit("swap", i, "")
        return None
    if len(s) < len(t):  # t has one extra char; it must sit at the first mismatch
        return Edit("insert", i, t[i]) if s[i:] == t[i + 1:] else None
    return Edit("delete", i, "") if s[i + 1:] == t[i:] else None


def is_one_edit_distance(s: str, t: str) -> bool:
    """Part 1 (LC signature): exactly one insert/delete/replace turns s into t."""
    if abs(len(s) - len(t)) > 1:
        return False
    i = _first_mismatch(s, t)
    if len(s) == len(t):
        return i < len(s) and s[i + 1:] == t[i + 1:]  # i == len -> identical -> false
    short, long_ = (s, t) if len(s) < len(t) else (t, s)
    return short[i:] == long_[i + 1:]


def is_one_edit_or_swap(s: str, t: str) -> bool:
    """Part 2: Part 1, or one adjacent transposition of two different characters."""
    return find_edit(s, t) is not None


def within_k_edits(s: str, t: str, k: int) -> bool:
    """Part 4: Levenshtein distance <= k via a banded DP (only |i - j| <= k cells)."""
    n, m = len(s), len(t)
    if abs(n - m) > k:
        return False  # length difference alone needs more than k edits
    inf = k + 1
    width = 2 * k + 1  # row i holds j in [i - k, i + k] at offset d = j - (i - k)
    prev = [inf] * width
    for j in range(0, min(m, k) + 1):  # row 0: dp[0][j] = j
        prev[j + k] = j
    for i in range(1, n + 1):
        cur = [inf] * width
        base = i - k
        for d in range(width):
            j = base + d
            if j < 0 or j > m:
                continue
            if j == 0:
                cur[d] = i
                continue
            # prev[j-1] is prev[d]; prev[j] is prev[d+1]; cur[j-1] is cur[d-1]
            best = prev[d] + (s[i - 1] != t[j - 1])
            if d + 1 < width and prev[d + 1] + 1 < best:
                best = prev[d + 1] + 1
            if d >= 1 and cur[d - 1] + 1 < best:
                best = cur[d - 1] + 1
            cur[d] = best if best < inf else inf
        if min(cur) > k:
            return False  # every path already exceeds k
        prev = cur
    d = m - (n - k)
    return 0 <= d < width and prev[d] <= k


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.rstrip("\r") for ln in stdin.read().split("\n")]
    if not lines or not lines[0].strip():
        return
    part = int(lines[0].split()[1])
    k, rest = 0, lines[1:]
    if rest and rest[0].strip().upper().startswith("K "):
        k, rest = int(rest[0].split()[1]), rest[1:]
    s = rest[0].strip() if len(rest) > 0 else ""
    t = rest[1].strip() if len(rest) > 1 else ""
    if part == 1:
        out = str(is_one_edit_distance(s, t)).lower()
    elif part == 2:
        out = str(is_one_edit_or_swap(s, t)).lower()
    elif part == 3:
        e = find_edit(s, t)
        out = "none" if e is None else " ".join(str(x) for x in (e.kind, e.index, e.char) if x != "")
    else:
        out = str(within_k_edits(s, t, k)).lower()
    stdout.write(out + "\n")


if __name__ == "__main__":
    main()
