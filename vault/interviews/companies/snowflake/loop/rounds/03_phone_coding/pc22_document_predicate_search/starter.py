"""pc22 Document Predicate Search Engine -- YOUR implementation. Run the tests against this
file with IMPL=starter.

Maintain an inverted index (word -> set of doc ids) so queries are answered by set algebra, not
by scanning every document.
"""

from __future__ import annotations

import sys


class DocumentIndex:
    def __init__(self) -> None:
        # TODO
        pass

    def insert_doc(self, doc_id: int, words: list[str]) -> None:
        """Part1. Re-inserting an existing id replaces that document."""
        # TODO
        pass

    def delete_doc(self, doc_id: int) -> None:
        """Part3. No-op if doc_id was never inserted."""
        # TODO
        pass

    def check_contains_or(self, query: str) -> list[int]:
        """Part1: OR over the space-separated words in `query`."""
        # TODO
        return []

    def check_contains_bool(self, query: str) -> list[int]:
        """Part2: AND/OR with AND binding tighter. NOT and parentheses -> ValueError."""
        # TODO
        return []

    def check_contains_full(self, query: str) -> list[int]:
        """Part3: full grammar (AND/OR/NOT/parentheses)."""
        # TODO
        return []


def part1(lines: list[str]) -> list[str]:
    """commands: 'INSERT_DOC id w1 w2 ...' / 'CHECK_CONTAINS "a b c"' (OR over words) -> one
    output line per CHECK_CONTAINS: matching ids space-separated (ascending), or 'NONE'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """adds 'DELETE_DOC id'; CHECK_CONTAINS supports NOT and parentheses."""
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
