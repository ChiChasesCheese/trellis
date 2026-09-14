"""cd01 Subscription email scheduler — YOUR implementation.

Public API (must match solution.py):
    part1(lines) -> list[str]   # subscribe only
    part2(lines) -> list[str]   # + change (proration)
    part3(lines) -> list[str]   # + renew, cancel
    main(stdin=sys.stdin, stdout=sys.stdout) -> None

See problem.md for the exact input grammar, the discard-then-reschedule rule, and the
`date user email_type` output format (sorted by date, user, then a fixed email-type priority).
"""

from __future__ import annotations

import sys

PERIOD_DAYS = {"monthly": 30, "annual": 365}
TYPE_ORDER = {"welcome": 0, "expiring": 1, "expired": 2, "renewed": 3, "canceled": 4}


def part1(lines: list[str]) -> list[str]:
    """Only `subscribe` events: welcome@date, expiring@(expire-7), expiring@(expire-1),
    expired@expire. `expire = date + period_days(plan)`."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """part1 + `change,new_plan`: reprorate the remaining days onto the new plan's period and
    reschedule any not-yet-due expiring/expired emails."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """part2 + `renew` (extend from the old expiry, or start fresh if already past it) and
    `cancel` (wipe all future pending emails)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = 3
    if lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
