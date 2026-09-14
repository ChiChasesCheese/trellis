"""cd03 AccountScheduler — YOUR implementation. Run: pytest against this file with IMPL=starter.

See problem.md for the full contract (exception policy, exclusive lock end, LRU tie-break order).
"""

from __future__ import annotations

import sys


class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None:
        pass  # TODO: store accounts, a construction-order index, locked_until, last_used

    def is_available(self, account_id: str, t: int) -> bool:
        """Unknown account_id -> KeyError. Else True iff never locked or t >= locked_until."""
        raise NotImplementedError  # TODO

    def acquire(self, account_id: str, t: int, duration: int) -> bool:
        """duration <= 0 -> ValueError (checked before the unknown-id check). Lock [t, t+duration)
        and return True if available at t; else return False, no state change."""
        raise NotImplementedError  # TODO

    def acquire_any(self, t: int, duration: int) -> str | None:
        """duration <= 0 -> ValueError. Among accounts available at t: never-acquired first
        (construction order), then oldest last_used, ties -> construction order. Locks the
        winner and returns its id; None if nothing is available."""
        raise NotImplementedError  # TODO


def run_commands(lines: list[str]) -> list[str]:
    """First line 'ACCOUNTS id1 id2 ...' builds the scheduler; then AVAIL/ACQ/ANY commands.
    Malformed lines / KeyError / ValueError -> 'ERROR', processing continues."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = run_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
