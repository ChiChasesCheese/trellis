"""q31 Wishlist / Mutual Rank — YOUR implementation. Run: python drill.py test q31"""
from __future__ import annotations

import sys


class Wishlists:
    def __init__(self, data: dict[str, list[str]]) -> None:
        self.lists = data

    def has_mutual_first_choice(self, user: str) -> bool:
        # TODO
        return False

    def has_mutual_pair_for_rank(self, user: str, rank: int) -> bool:
        # TODO
        return False

    def changed_pairings(self, user: str, rank: int) -> list[str]:
        """Users whose pairing with `user` would gain/lose mutual-rank status if entry `rank` moved up."""
        # TODO
        return []

    def mutual_pairs(self) -> list[tuple[str, str, int]]:
        """All (u, v, score) with u < v, v in list[u], u in list[v]; sorted by score, u, v."""
        # TODO
        return []

    def best_match(self, user: str) -> tuple[str, int] | None:
        # TODO
        return None

    def cycles(self, k: int) -> list[list[str]]:
        """Simple cycles of length k, each rotated to start at its smallest name, sorted."""
        # TODO
        return []


def parse(lines: list[str]) -> tuple[Wishlists, list[list[str]]]:
    """Lines with ':' are wishlists, the rest are queries (split into tokens)."""
    # TODO
    return Wishlists({}), []


def part1(lines: list[str]) -> list[str]:
    """FIRST u / RANK u r -> 'true' | 'false'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """+ BUMP u r -> affected users or 'NONE'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """+ PAIRS -> 'u v score' lines; BEST u -> 'v score' | 'NONE'."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """+ CYCLES k -> 'u1 u2 ... uk' lines | 'NONE'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
