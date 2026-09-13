"""q35 User Points — YOUR implementation. Run: python drill.py test q35

Part 1 add + balances -> Part 2 spend FIFO by timestamp -> Part 3 negative transactions
cancel the payer's oldest positive points -> Part 4 atomic spend, ValueError when insufficient.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone


def parse_ts(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


class PointsAccount:
    def __init__(self) -> None:
        self.entries: list[list] = []      # [ts, seq, payer, remaining_points]
        self.balance: dict[str, int] = {}  # payer -> balance, first-add order

    def add(self, payer: str, points: int, timestamp: str) -> None:
        # TODO (raise ValueError if the payer's balance would go negative)
        pass

    def spend(self, points: int) -> list[tuple[str, int]]:
        """[(payer, -deducted), ...] in order of first consumption. ValueError if insufficient."""
        # TODO
        return []

    def balances(self) -> dict[str, int]:
        return dict(self.balance)


def process(lines: list[str]) -> list[str]:
    """ADD,payer,points,ts / SPEND,n / BALANCE -> output lines (see problem.md)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
