"""ps01 Transaction Stream Levels — reference solution.

Four unlock-next-part levels over the same input shape (`user_id,amount,timestamp`):
  Part 1: per-user totals (order-independent grouping).
  Part 2: "which users ever hit >= T within a W-second window" — one deque per user.
  Part 3: "top K users by 60s-window sum as of time t" — Part 1's totals over a filtered stream.
  Part 4: "[small, large, small] pattern" over each user's timestamp-ordered stream.

Amounts/timestamps are plain integers (no currency formatting here — see ps02 for money).
Every window is the **closed** interval [t - W, t] (both ends inclusive); problem.md "Rules"
explains why (the sourced Part 3 example only reproduces under a closed window).

Layout: parse (`_split_params`, `_parse_tx`) -> group (`_by_user_sorted`) -> one small helper
per part's core rule (`_totals`, `_first_crossing`, `_pattern_starts`) -> format in `partN`.
"""

from __future__ import annotations

import sys
from collections import defaultdict, deque
from typing import Iterable, NamedTuple

WINDOW_P3 = 60  # Part 3's window is fixed at 60s, not a parameter
DEFAULT_W = 60  # Part 2's window when the params line omits W
PATTERN = ("small", "large", "small")  # Part 4: the labels a run of consecutive txs must match


class Tx(NamedTuple):
    user: str
    amount: int
    ts: int
    order: int  # input index — tie-break for equal timestamps (keep input order)


# ------------------------------------------------------------------ parsing


def _split_params(lines: list[str]) -> tuple[dict[str, int], list[str]]:
    """Strip blanks; if the first line is a params line (`k=v k=v`, no comma), pop it.
    A data line always has exactly two commas, a params line none — that's the disambiguator."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    if lines and "," not in lines[0] and "=" in lines[0]:
        params = {k: int(v) for k, _, v in (tok.partition("=") for tok in lines[0].split())}
        return params, lines[1:]
    return {}, lines


def _parse_tx(lines: list[str]) -> list[Tx]:
    """`user_id,amount,timestamp` lines -> Tx records (fields tolerate surrounding spaces)."""
    out: list[Tx] = []
    for i, raw in enumerate(lines):
        user, amount, ts = (p.strip() for p in raw.split(","))
        out.append(Tx(user, int(amount), int(ts), i))
    return out


def _by_user_sorted(txs: Iterable[Tx]) -> dict[str, list[Tx]]:
    """user_id -> that user's transactions sorted by (timestamp, input order)."""
    grouped: dict[str, list[Tx]] = defaultdict(list)
    for tx in txs:
        grouped[tx.user].append(tx)
    for events in grouped.values():
        events.sort(key=lambda e: (e.ts, e.order))
    return grouped


# ------------------------------------------------------------------ core rules


def _totals(txs: Iterable[Tx]) -> dict[str, int]:
    """Sum of amount per user (Part 1's rule; Part 3 reuses it on a filtered stream)."""
    totals: dict[str, int] = defaultdict(int)
    for tx in txs:
        totals[tx.user] += tx.amount
    return totals


def _first_crossing(events: list[Tx], threshold: int, window: int) -> int | None:
    """Walk one user's sorted events with a deque; return the window sum at the FIRST moment
    the closed window [ts - W, ts] reaches >= threshold, or None if it never does."""
    live: deque[Tx] = deque()
    total = 0
    for tx in events:
        live.append(tx)
        total += tx.amount
        while live[0].ts < tx.ts - window:  # evict strictly older than W seconds (closed window)
            total -= live.popleft().amount
        if total >= threshold:
            return total
    return None


def _pattern_starts(events: list[Tx], split: int) -> list[int]:
    """Start timestamps of every run of consecutive events whose labels equal PATTERN
    (small := amount < split, large := amount >= split). Overlapping runs all count."""
    labels = ["small" if tx.amount < split else "large" for tx in events]
    n = len(PATTERN)
    return [events[i].ts for i in range(len(events) - n + 1) if tuple(labels[i : i + n]) == PATTERN]


# ------------------------------------------------------------------ parts (parse -> rule -> format)


def part1(lines: list[str]) -> list[str]:
    """Sum of amount per user, one 'user_id: total' per user, sorted by user_id (string order)."""
    _, body = _split_params(lines)
    totals = _totals(_parse_tx(body))
    return [f"{user}: {totals[user]}" for user in sorted(totals)]


def part2(lines: list[str]) -> list[str]:
    """Params 'T=<int> W=<int>' (W defaults to 60). Users whose closed [ts-W, ts] window sum ever
    reached >= T, as 'user_id: sum' (sum at the first crossing), sorted by user_id."""
    params, body = _split_params(lines)
    threshold, window = params["T"], params.get("W", DEFAULT_W)
    by_user = _by_user_sorted(_parse_tx(body))
    flagged = {user: _first_crossing(events, threshold, window) for user, events in by_user.items()}
    return [f"{user}: {total}" for user, total in sorted(flagged.items()) if total is not None]


def part3(lines: list[str]) -> list[str]:
    """Params 't=<int> K=<int>'. Top K users by sum over the closed window [t-60, t], ranked by
    sum desc then user_id asc, output in RANKED order. Users with no tx in the window are not
    candidates; fewer than K candidates -> print them all."""
    params, body = _split_params(lines)
    t, k = params["t"], params["K"]
    in_window = (tx for tx in _parse_tx(body) if t - WINDOW_P3 <= tx.ts <= t)
    ranked = sorted(_totals(in_window).items(), key=lambda kv: (-kv[1], kv[0]))
    return [f"{user}: {total}" for user, total in ranked[:k]]


def part4(lines: list[str]) -> list[str]:
    """Params 'S=<int>'. For each user (sorted by user_id) with at least one [small, large, small]
    run in timestamp order: 'user_id: t1,t2,...' (start timestamps ascending)."""
    params, body = _split_params(lines)
    by_user = _by_user_sorted(_parse_tx(body))
    out: list[str] = []
    for user in sorted(by_user):
        starts = _pattern_starts(by_user[user], params["S"])
        if starts:
            out.append(f"{user}: " + ",".join(map(str, starts)))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not raw:
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3, 4: part4}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
