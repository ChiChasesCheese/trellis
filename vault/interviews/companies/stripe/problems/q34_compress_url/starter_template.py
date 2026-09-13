"""q34 Compress URL — YOUR implementation. Run: python drill.py test q34

Part 1 numeronym per minor part -> Part 2 keep m minor parts (fold the tail, dots count)
-> Part 3 min_len threshold -> Part 4 ambiguity report.
"""
from __future__ import annotations

import sys


def numeronym(word: str, min_len: int = 0) -> str:
    """'stripe' -> 's4e'; min_len=0 always compresses; words shorter than min_len unchanged (Part 3)."""
    # TODO
    return word


def compress(url: str, m: int | None = None, min_len: int = 0) -> str:
    """Parts 1-3. m=None: no folding. Otherwise keep m-1 numeronyms and fold the rest."""
    # TODO
    return url


def ambiguous(urls: list[str]) -> list[str]:
    """Part 4: ['compressed: n', ...] for compressed forms shared by >= 2 distinct urls, sorted."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    return [compress(ln) for ln in lines]


def part2(lines: list[str]) -> list[str]:
    return [compress(u.strip(), int(m)) for u, m in (ln.rsplit(",", 1) for ln in lines)]


def part3(lines: list[str]) -> list[str]:
    return [compress(u.strip(), None, int(n)) for u, n in (ln.rsplit(",", 1) for ln in lines)]


def part4(lines: list[str]) -> list[str]:
    return ambiguous(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
