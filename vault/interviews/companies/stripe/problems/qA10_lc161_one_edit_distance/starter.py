"""qA10 LC 161 One Edit Distance — YOUR implementation. Run: python drill.py test qA10"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Edit(NamedTuple):
    kind: str    # "insert" | "delete" | "replace" | "swap"
    index: int   # position in s
    char: str    # inserted / replacement char; "" for delete and swap


def is_one_edit_distance(s: str, t: str) -> bool:
    """Part 1 (LC signature): exactly one insert/delete/replace turns s into t."""
    # TODO
    return False


def is_one_edit_or_swap(s: str, t: str) -> bool:
    """Part 2: Part 1, or one adjacent transposition of two different characters."""
    # TODO
    return False


def find_edit(s: str, t: str) -> Edit | None:
    """Part 3: the edit (index = first mismatch) turning s into t, swap allowed; None if not one edit."""
    # TODO
    return None


def within_k_edits(s: str, t: str, k: int) -> bool:
    """Part 4: Levenshtein distance <= k via a banded DP (only |i - j| <= k cells)."""
    # TODO
    return False


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().split("\n")
    # TODO: PART n / [K k] / s / t  (s and t may be empty lines)
    stdout.write("")


if __name__ == "__main__":
    main()
