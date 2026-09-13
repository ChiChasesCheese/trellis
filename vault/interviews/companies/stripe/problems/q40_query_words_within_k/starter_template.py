"""q40 Query Words Within k — YOUR implementation. Run: python drill.py test q40

Part 1 starts where every other query word occurs in (i, i+k] -> Part 2 minimal window (any
order, earliest on tie) -> Part 3 normalization -> Part 4 rank documents by window length.
"""
from __future__ import annotations

import re
import sys
from bisect import bisect_left
from collections import defaultdict

WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str, normalize: bool = False) -> list[str]:
    return WORD.findall(text.lower()) if normalize else text.split()


class Document:
    """Preprocessed text: tokens + word -> sorted positions (the interviewer's follow-up)."""

    def __init__(self, text: str, normalize: bool = False) -> None:
        self.tokens = tokenize(text, normalize)
        self.positions: dict[str, list[int]] = defaultdict(list)
        for i, w in enumerate(self.tokens):
            self.positions[w].append(i)


def find_starts(text: str, query: str, k: int, normalize: bool = False) -> list[int]:
    # TODO
    return []


def min_window(text: str, query: str, normalize: bool = False) -> tuple[int, int] | None:
    # TODO
    return None


def rank(docs: list[tuple[str, str]], query: str) -> list[tuple[str, int]]:
    # TODO
    return []


def process(lines: list[str], part: int) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out = process(lines[1:], part)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
