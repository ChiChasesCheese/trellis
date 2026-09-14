"""pc24 Service Failure Forensics -- YOUR implementation. Run the tests against this file with
IMPL=starter.

Three stages of one incident: binary search a sorted log for the first error, BFS/DFS the
services a failure cascades to, and the longest failure-propagation chain in that DAG.
"""

from __future__ import annotations

import sys


def first_error_at_or_after(logs: list[str], ts: str) -> int:
    """Part1: `logs` sorted by timestamp ascending, lines '<ts> <service> <LEVEL> [msg]'.
    Binary search for the first line with timestamp >= ts, then scan forward for the first
    ERROR. Return its index, or -1 if none. ValueError on an unknown LEVEL."""
    # TODO
    return -1


def services_that_will_fail(edges: list[str], initial_failure: str) -> list[str]:
    """Part2: edges are 'A B' meaning A depends on B (B fails -> A fails). BFS from
    initial_failure, returning every service that fails (including initial_failure) in BFS
    discovery order. ValueError if initial_failure never appears in any edge."""
    # TODO
    return []


def longest_failure_chain(edges: list[str]) -> list[str]:
    """Part3 (reconstructed): longest path in the failure DAG (B -> A). Ties broken by
    lexicographically-smallest full sequence. ValueError if edges is empty, or if the graph has
    a cycle (longest path is undefined on a cycle) -- name one service on the cycle."""
    # TODO
    return []


def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


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
