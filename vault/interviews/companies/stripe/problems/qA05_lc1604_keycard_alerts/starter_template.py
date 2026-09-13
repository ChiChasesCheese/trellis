"""qA05 LC 1604 Key-card alerts — YOUR implementation. Run: python drill.py test qA05"""
from __future__ import annotations

import sys


def alert_names(key_name: list[str], key_time: list[str]) -> list[str]:
    """Part 1: names with >= 3 uses inside any 60-minute window (inclusive); unique, sorted."""
    # TODO
    return []


def alert_names_k(key_name: list[str], key_time: list[str], k: int = 3, window: int = 60) -> list[str]:
    """Part 2: names with >= k uses inside any `window`-minute span (inclusive)."""
    # TODO
    return []


class KeyCardLimiter:
    """Part 3: allow a swipe iff fewer than `limit` ALLOWED swipes of that name lie in [t-window, t]."""

    def __init__(self, limit: int = 2, window: int = 60) -> None:
        self.limit, self.window = limit, window
        self.denied: list[tuple[str, str]] = []
        # TODO

    def swipe(self, name: str, time: str) -> bool:
        # TODO
        return True


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / [k window] / name HH:MM lines
    stdout.write("")


if __name__ == "__main__":
    main()
