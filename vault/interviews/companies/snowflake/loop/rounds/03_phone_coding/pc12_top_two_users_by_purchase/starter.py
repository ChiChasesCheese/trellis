"""pc12 Top Two Users by Total Purchase Amount -- YOUR implementation. Run tests with IMPL=starter.

See problem.md: amounts are ALWAYS parsed to integer cents by string surgery, never through float.
"""

from __future__ import annotations

import sys


def top_two_users(records: list[str]) -> list[tuple[str, int]]:
    """Part1: records 'user,amount' -> top two (user, cents) by total desc, tie user asc.
    Raise ValueError for a malformed record or a negative amount."""
    # TODO
    return []


def top_k_per_day(records: list[str], k: int) -> list[tuple[str, list[tuple[str, int]]]]:
    """Part2: records 'date,user,amount' -> [(date, top-k (user, cents) for that date), ...],
    dates ascending."""
    # TODO
    return []


def process_stream(events: list[str]) -> list[list[tuple[str, int]]]:
    """Part3: apply 'user,amount' updates in order (amount may be negative: a refund); each
    literal 'QUERY' event snapshots the current top-two. Returns the list of snapshots, in order."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """'N n' / n 'user,amount' lines -> up to two 'user cents' lines, or '-'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """'N n' / n 'date,user,amount' lines / 'K k' -> per date (ascending): 'date count' then
    up to k 'user cents' lines. '-' if there is no data at all."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """'N n' / n lines, each 'user,amount' or 'QUERY' -> per QUERY (in order): 'Q count' then up
    to two 'user cents' lines. '-' if there were no QUERY events at all."""
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
