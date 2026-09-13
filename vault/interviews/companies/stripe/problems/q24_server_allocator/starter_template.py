"""q24 Server Allocator — YOUR implementation. Run: python drill.py test q24"""
from __future__ import annotations

import heapq
import sys


def next_server_number(allocated) -> int:
    """Part 1: smallest positive integer not in `allocated` (ignore dups/0/negatives/non-ints)."""
    # TODO
    return 1


def split_hostname(hostname: str) -> tuple[str, int] | None:
    """'apibox12' -> ('apibox', 12); None if there is no trailing number or the number is 0."""
    # TODO
    return None


class Tracker:
    """Parts 2-3: per-type pools; allocate reuses the smallest freed number (heap), O(log n)."""

    def __init__(self, strict: bool = False) -> None:
        self.strict = strict
        self.next: dict[str, int] = {}          # type -> next never-used number
        self.free: dict[str, list[int]] = {}    # type -> min-heap of freed numbers
        self.live: set[str] = set()             # allocated hostnames

    def allocate(self, host_type: str) -> str:
        # TODO
        return ""

    def deallocate(self, hostname: str) -> bool:
        # TODO (unknown -> False, or KeyError when strict)
        return False


def run_commands(lines: list[str]) -> list[str]:
    """Part 4: 'ALLOCATE type' -> name printed; 'DEALLOCATE name' -> nothing."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines()]
    if not lines or not lines[0]:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    # TODO: PART 1 -> one number list per line; PART 2-4 -> commands
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
