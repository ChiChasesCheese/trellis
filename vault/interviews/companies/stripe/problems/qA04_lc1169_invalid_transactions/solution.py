"""qA04 LC 1169 Invalid Transactions — reference solution.

Group by name, sort by (time, index), slide an inclusive [t-60, t+60] window holding a city
counter: a transaction is city-invalid iff the window contains a different city. Amount rule is
independent. Output keeps input order so results are deterministic.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict, deque
from typing import NamedTuple

WINDOW = 60      # minutes, inclusive on both ends
AMOUNT_CAP = 1000  # amount > 1000 is invalid (== 1000 is fine)


class Tx(NamedTuple):
    index: int
    name: str
    time: int
    amount: int
    city: str
    raw: str


class Verdict(NamedTuple):
    index: int
    transaction: str
    reasons: list[str]


def parse(transactions: list[str]) -> list[Tx]:
    out = []
    for i, raw in enumerate(transactions):
        name, t, amt, city = (p.strip() for p in raw.strip().split(","))
        out.append(Tx(i, name, int(t), int(amt), city, raw.strip()))
    return out


def _city_conflicts(txs: list[Tx], window: int = WINDOW) -> dict[int, list[Tx]]:
    """index -> conflicting transactions (same name, other city, |dt| <= window), by (time, index).
    Uses a two-pointer window per name; only lists the pairs that exist (output-sensitive)."""
    by_name: dict[str, list[Tx]] = defaultdict(list)
    for tx in txs:
        by_name[tx.name].append(tx)
    conflicts: dict[int, list[Tx]] = defaultdict(list)
    for group in by_name.values():
        group.sort(key=lambda t: (t.time, t.index))
        lo = 0
        for i, tx in enumerate(group):
            while group[lo].time < tx.time - window:  # drop everything older than t-60
                lo += 1
            # window = group[lo:hi] with times in [t-60, t+60]; scan only as far as the window reaches
            for j in range(lo, len(group)):
                other = group[j]
                if other.time > tx.time + window:
                    break
                if other.city != tx.city:  # same city never conflicts (also handles duplicates)
                    conflicts[tx.index].append(other)
    return conflicts


def _is_city_invalid(txs: list[Tx], window: int = WINDOW) -> set[int]:
    """Same test in O(n log n): window counter of cities; invalid iff window holds another city."""
    by_name: dict[str, list[Tx]] = defaultdict(list)
    for tx in txs:
        by_name[tx.name].append(tx)
    bad: set[int] = set()
    for group in by_name.values():
        group.sort(key=lambda t: (t.time, t.index))
        cities: Counter[str] = Counter()
        lo = hi = 0
        for tx in group:
            while hi < len(group) and group[hi].time <= tx.time + window:  # extend to t+60 inclusive
                cities[group[hi].city] += 1
                hi += 1
            while group[lo].time < tx.time - window:  # shrink below t-60
                cities[group[lo].city] -= 1
                lo += 1
            if (hi - lo) - cities[tx.city] > 0:  # someone in the window is in another city
                bad.add(tx.index)
    return bad


def invalid_transactions(transactions: list[str]) -> list[str]:
    """Part 1: input order, duplicates preserved."""
    txs = parse(transactions)
    bad = _is_city_invalid(txs)
    return [tx.raw for tx in txs if tx.amount > AMOUNT_CAP or tx.index in bad]


def invalid_reasons(transactions: list[str]) -> list[Verdict]:
    """Part 2: 'amount>1000' first, then 'city:<other>' per conflict in (time, index) order."""
    txs = parse(transactions)
    conflicts = _city_conflicts(txs)
    out: list[Verdict] = []
    for tx in txs:
        reasons: list[str] = []
        if tx.amount > AMOUNT_CAP:
            reasons.append("amount>1000")
        reasons += [f"city:{o.raw}" for o in conflicts.get(tx.index, [])]
        if reasons:
            out.append(Verdict(tx.index, tx.raw, reasons))
    return out


class TransactionStream:
    """Part 3: arrivals in non-decreasing time; per-name deque of the last `window` minutes."""

    def __init__(self, window: int = WINDOW, cap: int = AMOUNT_CAP) -> None:
        self.window, self.cap = window, cap
        self.flagged: list[str] = []
        self._seen: set[int] = set()            # arrival ids already reported
        self._recent: dict[str, deque[Tx]] = defaultdict(deque)
        self._count = 0
        self._last_time = -1

    def add(self, transaction: str) -> list[str]:
        tx = parse([transaction])[0]._replace(index=self._count)
        self._count += 1
        if tx.time < self._last_time:
            raise ValueError(f"out-of-order arrival: {transaction!r} after t={self._last_time}")
        self._last_time = tx.time
        q = self._recent[tx.name]
        while q and q[0].time < tx.time - self.window:  # t-60 itself is still inside
            q.popleft()
        newly: list[Tx] = []
        conflict = False
        for other in q:  # deque is already in (time, arrival) order
            if other.city != tx.city:
                conflict = True
                if other.index not in self._seen:
                    newly.append(other)
        if conflict or tx.amount > self.cap:
            newly.append(tx)
        q.append(tx)
        out = []
        for t in newly:
            self._seen.add(t.index)
            self.flagged.append(t.raw)
            out.append(t.raw)
        return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    txs = lines[1:]
    if part == 1:
        out = invalid_transactions(txs)
    elif part == 2:
        out = [f"{v.transaction} | " + " ; ".join(v.reasons) for v in invalid_reasons(txs)]
    else:
        stream = TransactionStream()
        out = []
        for t in txs:
            got = stream.add(t)
            if got:
                out.append(f"{t} => " + " ; ".join(got))
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
