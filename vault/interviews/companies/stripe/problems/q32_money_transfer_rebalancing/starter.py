"""q32 Money Transfer / Rebalancing — YOUR implementation. Run: python drill.py test q32"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Account(NamedTuple):
    name: str
    balance: int


class Transfer(NamedTuple):
    src: str
    dst: str
    amount: int

    def __str__(self) -> str:
        return f"from: {self.src}, to: {self.dst}, amount: {self.amount}"


def rebalance_in_order(accounts: list[Account], minimum: int = 100) -> list[Transfer] | None:
    """Input-order greedy; None when sum(balances) < minimum * len(accounts)."""
    # TODO
    return None


def rebalance_greedy(accounts: list[Account], minimum: int = 100, fee: int = 0) -> list[Transfer] | None:
    """Largest surplus -> largest deficit two-pointer (heuristic); sender also pays `fee` per transfer."""
    # TODO
    return None


def min_transfers_exact(accounts: list[Account], minimum: int = 100) -> list[Transfer] | None:
    """Fewest transfers (DFS + branch and bound, <= 12 non-zero accounts). None when impossible."""
    # TODO
    return None


def apply_transfers(accounts: list[Account], transfers: list[Transfer], minimum: int = 100) -> tuple[list[Account], str]:
    """-> (final balances in input order, verdict in {OK, INCOMPLETE, BEST_EFFORT, NOT_BEST_EFFORT, INVALID})."""
    # TODO
    return accounts, "INVALID"


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 1
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
