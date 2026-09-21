"""pc07 Anagram Store -- YOUR implementation. Run the tests against this file with IMPL=starter.

Warm-up (LC 20, Valid Parentheses) + a data structure that groups strings by anagram, with
increasingly rich queries across the three parts.
"""

from __future__ import annotations

import sys


def is_valid_parentheses(s: str) -> bool:
    """Warm-up (LC 20). s must contain only '()[]{}' -> ValueError otherwise."""
    # TODO
    return False


def canonical_key_sorted(word: str) -> str:
    """Part1: sort word's characters into a string. O(L log L), any alphabet."""
    # TODO
    return ""


def canonical_key_counts(word: str) -> tuple[int, ...]:
    """Part1: 26-slot a-z count vector. O(L), only lowercase a-z -> ValueError otherwise."""
    # TODO
    return tuple()


class AnagramStore:
    """Groups added words by anagram, using canonical_key_sorted internally."""

    def __init__(self, case_sensitive: bool = True) -> None:
        # TODO
        self.case_sensitive = case_sensitive

    def add(self, word: str) -> None:
        """Part1: append word to its anagram group (insertion order; duplicates allowed)."""
        # TODO
        raise NotImplementedError

    def group_of(self, word: str) -> list[str]:
        """Part1: words sharing word's anagram group, insertion order; [] if none."""
        # TODO
        return []

    def count(self, word: str) -> int:
        """Part1: len(group_of(word))."""
        # TODO
        return 0

    def remove(self, word: str) -> None:
        """Part2: remove ONE literal occurrence of word from its group. ValueError if absent."""
        # TODO
        raise NotImplementedError

    def most_common_group(self) -> list[str]:
        """Part2: the group with the most members; [] if store empty; tie -> smallest key."""
        # TODO
        return []

    def top_k_groups(self, k: int) -> list[list[str]]:
        """Part3: the k largest groups, desc size then key asc. k must be a positive int."""
        # TODO
        return []


def part1(lines: list[str]) -> list[str]:
    """ops: 'ADD <word>' / 'GROUP <word>' / 'COUNT <word>'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """part1 ops plus 'REMOVE <word>' / 'MOSTCOMMON'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines[0] = 'CASE SENSITIVE'|'CASE INSENSITIVE', then 'ADD <word>' / 'TOPK <k>'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
