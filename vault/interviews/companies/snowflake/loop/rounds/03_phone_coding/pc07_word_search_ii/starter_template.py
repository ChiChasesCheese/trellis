"""pc07 Word Search II -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: board is a rectangular grid of lowercase letters; a word is a path of adjacent
(up/down/left/right, no diagonals) cells that never reuses a cell within the same path.
"""

from __future__ import annotations

import sys


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """Part1 (LC 212): words from `words` that can be traced on `board`, sorted ascending.
    Raise ValueError for a malformed board or an invalid word."""
    # TODO
    return []


def find_words_with_paths(
    board: list[list[str]], words: list[str]
) -> list[tuple[str, list[tuple[int, int]]]]:
    """Part2: (word, first path) pairs sorted by word ascending. "First" = row-major start cells,
    neighbours tried UP, DOWN, LEFT, RIGHT."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'R C' / R board rows / 'W k' / k words -> one line: found words asc, space-separated, or '-'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same input -> one line per found word (asc): 'word r,c r,c ...'; '-' if none found."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
