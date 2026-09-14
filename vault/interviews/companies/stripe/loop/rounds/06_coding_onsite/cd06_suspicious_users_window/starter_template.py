"""cd06 Suspicious Users Sliding Window — YOUR implementation."""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """lines: raw 'user_id,amount,timestamp' rows, possibly out of order. A user is suspicious if
    any 60s window [t-60, t] anchored at one of their own transactions t contains >= 4 of their
    transactions (counting t). Return suspicious user_ids, sorted (plain string order). O(n^2)
    per user is fine for this part."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same detection rule, but O(n log n) overall (sort, then a per-user two-pointer scan).
    Return one line per suspicious user: 'user_id: <count> in [<start_ts>, <end_ts>]' for that
    user's FIRST (earliest, in time order) triggering window."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    lines = [ln for ln in rest.splitlines() if ln.strip()]
    out = part1(lines) if part == 1 else part2(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
