"""cd06 Suspicious Users Sliding Window — reference solution.

Window is the closed interval [t-60, t] anchored at each transaction t (see problem.md). Both
parts share one O(n log n) engine (`_first_triggers`): sort every user's timestamps once, then a
per-user two-pointer scan finds the first t whose trailing window first reaches >=4 transactions.
Part 1 is allowed to be a naive O(n^2) per-user scan in an interview; the reference solution reuses
the efficient engine for both parts since it is strictly cheaper and produces identical results.
"""

from __future__ import annotations

import sys
from collections import defaultdict

WINDOW_SECONDS = 60
MIN_COUNT = 4  # "more than 3" == ">= 4"


def _parse(lines: list[str]) -> dict[str, list[int]]:
    """user_id -> [timestamp, ...] in original input order (not yet sorted)."""
    by_user: dict[str, list[int]] = defaultdict(list)
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        user, _amount, ts = (p.strip() for p in raw.split(","))
        by_user[user].append(int(ts))
    return by_user


def _first_trigger(timestamps: list[int]) -> tuple[int, int, int] | None:
    """timestamps: one user's timestamps, already sorted ascending.

    Returns (start_ts, end_ts, count) for the first window (in ascending time order) whose count
    reaches MIN_COUNT, or None if the user is never suspicious. Two-pointer: `i` only ever moves
    forward, so this is O(n) after the sort.
    """
    i = 0
    for j, t in enumerate(timestamps):
        while t - timestamps[i] > WINDOW_SECONDS:
            i += 1
        count = j - i + 1
        if count >= MIN_COUNT:
            return timestamps[i], t, count
    return None


def _first_triggers(lines: list[str]) -> dict[str, tuple[int, int, int]]:
    """user_id -> (start_ts, end_ts, count) for every suspicious user."""
    by_user = _parse(lines)
    triggers: dict[str, tuple[int, int, int]] = {}
    for user, timestamps in by_user.items():
        timestamps.sort()  # ties (equal timestamps) need no explicit tie-break: any order among
        # equal values yields the same window bounds and the same count.
        trigger = _first_trigger(timestamps)
        if trigger is not None:
            triggers[user] = trigger
    return triggers


def part1(lines: list[str]) -> list[str]:
    return sorted(_first_triggers(lines))


def part2(lines: list[str]) -> list[str]:
    triggers = _first_triggers(lines)
    return [f"{user}: {count} in [{start}, {end}]" for user, (start, end, count) in sorted(triggers.items())]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    lines = [ln for ln in rest.splitlines() if ln.strip()]
    out = part1(lines) if part == 1 else part2(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
