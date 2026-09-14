"""pc27 Recipe Sequence Matcher -- YOUR implementation. Run the tests against this file with
IMPL=starter.

A recipe "occurs" iff it appears as a CONTIGUOUS run inside ingredients (substring-of-a-sequence,
not subsequence). An empty recipe trivially occurs.
"""

from __future__ import annotations

import sys


def find_recipes(ingredients: list[str], recipes: list[list[str]]) -> list[bool]:
    """Part1: preprocessing over ingredients is allowed (e.g. a hash of positions per token)."""
    # TODO
    return [False for _ in recipes]


def find_recipes_o1_space(ingredients: list[str], recipe: list[str]) -> bool:
    """Part2: single recipe, O(1) AUXILIARY space -- no position index, no automaton, just a
    two-pointer restart scan."""
    # TODO
    return False


def find_recipes_trie(ingredients: list[str], recipes: list[list[str]]) -> list[bool]:
    """Part3 (reconstructed): many recipes sharing prefixes -- build a trie over all recipes,
    walk ingredients once per start position."""
    # TODO
    return [False for _ in recipes]


def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _tok(line: str) -> list[str]:
    return line.split() if line.strip() else []


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
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
