"""q35 User Points — reference solution.

Entries are mutable [ts, seq, payer, remaining]. Every spend sorts them by (ts, seq) — Timsort is
linear on the already-sorted prefix — nets pending negative transactions against that payer's
oldest positive entries (Part 3), then walks positives oldest-first (Part 2).
"""
from __future__ import annotations

import sys
from collections import defaultdict, deque
from datetime import datetime, timezone


def parse_ts(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)  # naive -> UTC so comparisons work


class PointsAccount:
    def __init__(self) -> None:
        self.entries: list[list] = []      # [ts, seq, payer, remaining_points]
        self.balance: dict[str, int] = {}  # payer -> balance, first-add order (dict keeps it)

    def add(self, payer: str, points: int, timestamp: str) -> None:
        if self.balance.get(payer, 0) + points < 0:   # Part 3: a payer never goes negative
            raise ValueError(f"{payer} would go negative")
        self.balance[payer] = self.balance.get(payer, 0) + points
        self.entries.append([parse_ts(timestamp), len(self.entries), payer, points])

    def _net_negatives(self) -> None:
        """Part 3: each negative entry (oldest first) cancels its payer's oldest remaining positives."""
        heads: dict[str, deque] = defaultdict(deque)
        for e in self.entries:
            if e[3] > 0:
                heads[e[2]].append(e)
        for e in self.entries:
            if e[3] < 0:
                need, q = -e[3], heads[e[2]]   # never runs dry: add() kept the payer's sum >= 0
                while need:
                    take = min(q[0][3], need)
                    q[0][3] -= take
                    need -= take
                    if q[0][3] == 0:
                        q.popleft()
                e[3] = 0

    def spend(self, points: int) -> list[tuple[str, int]]:
        if points < 0 or points > sum(self.balance.values()):  # Part 4: atomic, checked up front
            raise ValueError("insufficient points")
        self.entries.sort(key=lambda e: (e[0], e[1]))  # ties on timestamp: insertion order
        self._net_negatives()
        spent: dict[str, int] = {}                     # first consumption order
        need = points
        for e in self.entries:
            if need == 0:
                break
            if e[3] <= 0:
                continue
            take = min(e[3], need)
            e[3] -= take
            need -= take
            spent[e[2]] = spent.get(e[2], 0) + take
            self.balance[e[2]] -= take
        return [(p, -d) for p, d in spent.items()]

    def balances(self) -> dict[str, int]:
        return dict(self.balance)


def process(lines: list[str]) -> list[str]:
    acct, out = PointsAccount(), []
    for ln in lines:
        cmd, *args = [p.strip() for p in ln.split(",")]
        try:
            if cmd == "ADD":
                acct.add(args[0], int(args[1]), args[2])
            elif cmd == "SPEND":
                out.append(";".join(f"{p},{d}" for p, d in acct.spend(int(args[0]))))
            elif cmd == "BALANCE":
                out.append(";".join(f"{p},{b}" for p, b in acct.balances().items()))
        except ValueError:
            out.append("ERROR")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
