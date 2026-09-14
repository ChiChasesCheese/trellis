"""pc16 Reverse Alphanumeric Segments -- reference solution.

f treats the string as a sequence of maximal runs of alphanumeric characters separated by
"boundary" characters (anything for which str.isalnum() is False: punctuation, whitespace,
apostrophes, ...). Each run is reversed in place; boundary characters never move.
"We're" -> runs "We" and "re" (the apostrophe is a boundary) -> "eW" + "'" + "er" = "eW'er".

Part1 builds a new string (a two-pointer scan that reverses each run as it is copied).
Part2 is the interview follow-up: do it in place on a mutable sequence of characters with O(1)
extra space, and stay Unicode-aware (str.isalnum() is already Unicode-aware -- "café1" has one
run "café1" because 'é' is alphanumeric). (reconstructed follow-up)
"""

from __future__ import annotations

import sys


def reverse_alnum_segments(s: str) -> str:
    """Part1: reverse each maximal run of alphanumeric characters; other characters stay in
    place. O(n) time, O(n) extra space (a new string is built)."""
    chars = list(s)
    _reverse_runs_inplace(chars)
    return "".join(chars)


def reverse_alnum_segments_inplace(chars: list) -> None:
    """Part2: same transformation, mutating `chars` (a list of single-character strings) in
    place. O(n) time, O(1) extra space beyond the input list itself. Unicode-aware because it
    relies on str.isalnum()."""
    _reverse_runs_inplace(chars)


def _reverse_runs_inplace(chars: list) -> None:
    n = len(chars)
    i = 0
    while i < n:
        if not chars[i].isalnum():
            i += 1
            continue
        j = i
        while j < n and chars[j].isalnum():
            j += 1
        lo, hi = i, j - 1
        while lo < hi:
            chars[lo], chars[hi] = chars[hi], chars[lo]
            lo += 1
            hi -= 1
        i = j


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """one string per line -> its transformed form, one per line."""
    return [reverse_alnum_segments(line) for line in lines]


def part2(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        chars = list(line)
        reverse_alnum_segments_inplace(chars)
        out.append("".join(chars))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """Blank lines are significant input (the empty string), so unlike other pc* problems this
    does NOT drop blank lines -- only the first 'PART <n>' line is special."""
    raw = stdin.read().splitlines()
    if not raw or not raw[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(raw[0].split()[1])
    out = {1: part1, 2: part2}[n](raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
