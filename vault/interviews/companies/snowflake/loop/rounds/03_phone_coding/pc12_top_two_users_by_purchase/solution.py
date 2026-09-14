"""pc12 Top Two Users by Total Purchase Amount -- reference solution.

Money is always parsed straight to integer CENTS by string surgery (never through float): an
amount looks like `"12.34"` (exactly two decimal digits, optional leading sign) and becomes
`1234`. Every output amount is cents, never a re-rendered dollar string -- see CONVENTIONS.md.

Part1 (LC-style original): records are `"user,amount"`; sum per user; return the top two users by
total amount descending, ties broken by username ascending (fewer than two distinct users -> fewer
results).

Part2 (reconstructed): records are `"date,user,amount"`; group by date, then within each date
report the top-k users by that day's total (same descending-total / ascending-username order).

Part3 (reconstructed): a single stream of events, each either an amount update (`"user,amount"`,
where a negative amount is a REFUND against that user's running total) or a `"QUERY"` marker that
snapshots the current top-two at that point in the stream. Refunds can push a user's running total
to zero or negative; they stay in the ranking (a user with a negative total can still be one of the
top two if nobody else is even).
"""

from __future__ import annotations

import re
import sys

_AMOUNT_RE = re.compile(r"\d+\.\d{2}")


def _parse_cents(amount: str, *, allow_negative: bool) -> int:
    s = amount.strip()
    sign = 1
    if s.startswith("-"):
        if not allow_negative:
            raise ValueError(f"amount must be non-negative, got {amount!r}")
        sign = -1
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if not _AMOUNT_RE.fullmatch(s):
        raise ValueError(f"amount must look like '12.34' (exactly two decimal digits), got {amount!r}")
    whole, frac = s.split(".")
    return sign * (int(whole) * 100 + int(frac))


def _ranked(totals: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(totals.items(), key=lambda p: (-p[1], p[0]))


# --------------------------------------------------------------------------- Part 1
def top_two_users(records: list[str]) -> list[tuple[str, int]]:
    totals: dict[str, int] = {}
    for rec in records:
        parts = rec.split(",")
        if len(parts) != 2:
            raise ValueError(f"record must be 'user,amount', got {rec!r}")
        user, amount = parts[0].strip(), parts[1]
        if not user:
            raise ValueError(f"user must be non-empty, got {rec!r}")
        cents = _parse_cents(amount, allow_negative=False)
        totals[user] = totals.get(user, 0) + cents
    return _ranked(totals)[:2]


# --------------------------------------------------------------------------- Part 2
def top_k_per_day(records: list[str], k: int) -> list[tuple[str, list[tuple[str, int]]]]:
    if k < 0:
        raise ValueError("k must be >= 0")
    per_day: dict[str, dict[str, int]] = {}
    for rec in records:
        parts = rec.split(",")
        if len(parts) != 3:
            raise ValueError(f"record must be 'date,user,amount', got {rec!r}")
        date, user, amount = parts[0].strip(), parts[1].strip(), parts[2]
        if not date or not user:
            raise ValueError(f"date and user must be non-empty, got {rec!r}")
        cents = _parse_cents(amount, allow_negative=False)
        totals = per_day.setdefault(date, {})
        totals[user] = totals.get(user, 0) + cents
    return [(date, _ranked(per_day[date])[:k]) for date in sorted(per_day)]


# --------------------------------------------------------------------------- Part 3
def process_stream(events: list[str]) -> list[list[tuple[str, int]]]:
    """Apply `"user,amount"` updates (amount may be negative: a refund) in order; each literal
    `"QUERY"` event snapshots the current top-two into the returned list."""
    totals: dict[str, int] = {}
    snapshots: list[list[tuple[str, int]]] = []
    for ev in events:
        if ev.strip() == "QUERY":
            snapshots.append(_ranked(totals)[:2])
            continue
        parts = ev.split(",")
        if len(parts) != 2:
            raise ValueError(f"event must be 'user,amount' or 'QUERY', got {ev!r}")
        user, amount = parts[0].strip(), parts[1]
        if not user:
            raise ValueError(f"user must be non-empty, got {ev!r}")
        cents = _parse_cents(amount, allow_negative=True)
        totals[user] = totals.get(user, 0) + cents
    return snapshots


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _fmt_ranked(ranked: list[tuple[str, int]]) -> list[str]:
    return [f"{user} {cents}" for user, cents in ranked] if ranked else ["-"]


def part1(lines: list[str]) -> list[str]:
    """'N n' / n 'user,amount' lines -> up to two 'user cents' lines, or '-'."""
    records, _ = _read_n_lines(lines, 0)
    return _fmt_ranked(top_two_users(records))


def part2(lines: list[str]) -> list[str]:
    """'N n' / n 'date,user,amount' lines / 'K k' -> per date (ascending): 'date count' then
    up to k 'user cents' lines. '-' if there is no data at all."""
    records, idx = _read_n_lines(lines, 0)
    tag, k = lines[idx].split()
    if tag != "K":
        raise ValueError(f"expected 'K <k>', got {lines[idx]!r}")
    per_day = top_k_per_day(records, int(k))
    if not per_day:
        return ["-"]
    out: list[str] = []
    for date, ranked in per_day:
        out.append(f"{date} {len(ranked)}")
        out.extend(f"{user} {cents}" for user, cents in ranked)
    return out


def part3(lines: list[str]) -> list[str]:
    """'N n' / n lines, each 'user,amount' or 'QUERY' -> per QUERY (in order): 'Q count' then up
    to two 'user cents' lines. '-' if there were no QUERY events at all."""
    events, _ = _read_n_lines(lines, 0)
    snapshots = process_stream(events)
    if not snapshots:
        return ["-"]
    out: list[str] = []
    for snap in snapshots:
        out.append(f"Q {len(snap)}")
        out.extend(f"{user} {cents}" for user, cents in snap)
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
