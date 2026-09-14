"""pc11 Character Frequencies -- YOUR implementation. Run the tests against this file with IMPL=starter.

See problem.md: count every character (spaces and punctuation included), sort by (count desc, char
asc). Part2/3 accept arbitrarily deep nested lists of strings -- flatten ITERATIVELY, not recursively.
"""

from __future__ import annotations

import sys


def char_frequencies(strings: list[str]) -> list[tuple[str, int]]:
    """Part1: (char, count) pairs across a flat list of strings, sorted (count desc, char asc).
    Raise ValueError if `strings` contains anything other than str."""
    # TODO
    return []


def char_frequencies_nested(data: list) -> list[tuple[str, int]]:
    """Part2: same as Part1 but `data` is an arbitrarily deep nested list of strings.
    Must flatten iteratively (explicit stack), not recursively."""
    # TODO
    return []


def top_k_chars(data: list, k: int) -> list[tuple[str, int]]:
    """Part3: top-k (count desc, char asc), with ties at the cutoff included."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'N n' / n string lines -> one 'char count' line per char (desc count, asc char), or '-'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """One line: a nested-list literal of strings -> same output format as part1."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'K k' / one line: a nested-list literal -> top-k chars (ties included), same output format."""
    # TODO
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
