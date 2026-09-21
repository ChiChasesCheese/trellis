"""pc09 Price Data Store -- candidate starter.

Fill in PriceStore, FXTable, price_in_base and part1/part2/part3 below. See problem.md for the
full API contract, rules and worked examples.
"""

from __future__ import annotations

import sys
from decimal import Decimal


class PriceStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def upsert(self, symbol: str, ts: int, price, volume=0) -> None:
        raise NotImplementedError

    def latest(self, symbol: str) -> Decimal:
        raise NotImplementedError

    def as_of(self, symbol: str, ts: int) -> Decimal:
        raise NotImplementedError

    def ohlc(self, symbol: str, t0: int, t1: int) -> tuple[Decimal, Decimal, Decimal, Decimal]:
        raise NotImplementedError

    def vwap(self, symbol: str, t0: int, t1: int) -> Decimal:
        raise NotImplementedError


class FXTable:
    def __init__(self) -> None:
        raise NotImplementedError

    def upsert(self, pair: str, ts: int, rate) -> None:
        raise NotImplementedError

    def rate_as_of(self, pair: str, ts: int) -> Decimal:
        raise NotImplementedError


def price_in_base(store: PriceStore, fx: FXTable, symbol: str, ts: int, symbol_ccy: str, base_ccy: str) -> Decimal:
    raise NotImplementedError


def part1(lines: list[str]) -> list[str]:
    return []


def part2(lines: list[str]) -> list[str]:
    return []


def part3(lines: list[str]) -> list[str]:
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
