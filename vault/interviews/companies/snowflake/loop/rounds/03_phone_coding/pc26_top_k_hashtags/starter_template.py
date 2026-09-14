"""pc26 Top K Hashtags -- YOUR implementation. Run the tests against this file with IMPL=starter.

Popularity of a hashtag = number of DISTINCT users who have ever posted it, not total post count.
"""

from __future__ import annotations

import sys


def top_k_hashtags(events: list[tuple[str, str]], k: int) -> list[tuple[str, int]]:
    """Part1: events are (user_id, hashtag). Popularity = distinct users per hashtag. Return up
    to k (hashtag, popularity), sorted popularity desc then hashtag asc. ValueError if k < 0."""
    # TODO
    return []


class HashtagCounter:
    """Part2 (reconstructed): streaming add(user, tag) + frequent top(k) queries."""

    def __init__(self) -> None:
        # TODO
        pass

    def add(self, user: str, tag: str) -> None:
        # TODO
        pass

    def top(self, k: int) -> list[tuple[str, int]]:
        # TODO
        return []


def top_k_hashtags_windowed(
    events: list[tuple[int, str, str]], k: int, window_seconds: int
) -> list[tuple[str, int]]:
    """Part3 (reconstructed): events are (timestamp, user_id, hashtag), not necessarily sorted.
    Only events with timestamp in the CLOSED window [max_ts - window_seconds, max_ts] count
    (max_ts = the largest timestamp across all events). A user counts once per tag within the
    window. ValueError if k < 0 or window_seconds < 0."""
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
