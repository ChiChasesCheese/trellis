"""q02 Vowel-Run DP — YOUR implementation. Run: python drill.py test q02"""
from __future__ import annotations

import sys

VOWELS = frozenset("aeiou")
MOD = 1_000_000_007


def part1(n: int, k: int) -> int:
    """Exact count (no modulus) of length-n strings (26-letter alphabet) with no run of more
    than k consecutive vowels."""
    # TODO
    return 0


def part2(word_len: int, max_vowels: int) -> int:
    """Same as part1 but mod 1_000_000_007, and must stay fast for word_len up to 2500."""
    # TODO
    return 0


def part3(s: str) -> int:
    """Count substrings of s that are entirely vowels AND contain all 5 distinct vowels."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format: first line 'PART n'; second line is the part's payload:
    PART 1 / PART 2 -> 'n k' (two ints, space-separated); PART 3 -> the raw string s
    (may be empty, i.e. the second line may be blank or absent). Output: a single integer
    line (no trailing content, no debug output)."""
    lines = stdin.read().split("\n")
    if not lines or lines[0].strip() == "":
        stdout.write("")
        return
    first = lines[0].strip()
    if not first.upper().startswith("PART"):
        raise ValueError("first line must be 'PART n'")
    part = int(first.split()[1])
    payload = lines[1] if len(lines) > 1 else ""
    if part == 1:
        n, k = (int(x) for x in payload.split())
        out = str(part1(n, k))
    elif part == 2:
        word_len, max_vowels = (int(x) for x in payload.split())
        out = str(part2(word_len, max_vowels))
    elif part == 3:
        out = str(part3(payload.rstrip("\r")))
    else:
        raise ValueError(f"unknown part {part}")
    stdout.write(out + "\n")


if __name__ == "__main__":
    main()
