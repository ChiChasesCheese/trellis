"""od05 Cron Scheduler -- YOUR implementation. Run pytest against this file with IMPL=starter.

See problem.md for the full contract: the */n-or-fixed-field cron subset, the pause-vs-claim
atomicity requirement, and the multi-instance LeaseStore for Part3.
"""

from __future__ import annotations

import sys
import threading
from datetime import datetime, timezone


def _field_match(field: str, value: int) -> bool:
    """'*' matches anything; '*/n' matches value % n == 0; a bare integer matches exactly."""
    if field == "*":
        return True
    if field.startswith("*/"):
        return value % int(field[2:]) == 0
    return int(field) == value


def _matches(cron_expr: str, now: int) -> bool:
    """now is minutes-since-epoch. cron_expr is 'minute hour day month weekday' (5 fields)."""
    minute_f, hour_f, day_f, month_f, weekday_f = cron_expr.split()
    dt = datetime.fromtimestamp(now * 60, tz=timezone.utc)
    return (
        _field_match(minute_f, dt.minute)
        and _field_match(hour_f, dt.hour)
        and _field_match(day_f, dt.day)
        and _field_match(month_f, dt.month)
        and _field_match(weekday_f, dt.weekday())  # Monday=0 .. Sunday=6
    )


class LeaseStore:
    def __init__(self) -> None:
        pass  # TODO: a shared claimed-(job_id, minute) set + a lock

    def try_claim(self, job_id: str, minute: int) -> bool:
        """First caller for a given (job_id, minute) gets True; every later caller (same or a
        different CronScheduler instance) gets False. Must be atomic under concurrent callers."""
        raise NotImplementedError  # TODO


class CronScheduler:
    def __init__(self, lease_store: "LeaseStore | None" = None) -> None:
        pass  # TODO: jobs, paused set, a lock, and (if lease_store is None) a local claim set

    def schedule(self, job_id: str, cron_expr: str) -> None:
        """(Re-)register a job: unpaused, no claim history changes for other minutes."""
        raise NotImplementedError  # TODO

    def pause(self, job_id: str) -> None:
        """Unknown job_id -> silently ignored (no exception)."""
        raise NotImplementedError  # TODO

    def resume(self, job_id: str) -> None:
        """Unknown job_id -> silently ignored (no exception)."""
        raise NotImplementedError  # TODO

    def tick(self, now: int) -> list[str]:
        """For every registered, unpaused job whose cron_expr matches `now`'s calendar fields:
        claim (job_id, now) exactly once (via self._lease_store if given, else a local claim
        set) and include it in the result iff this call won the claim. The paused-check and the
        claim must be atomic together for a single instance (see problem.md Part2)."""
        raise NotImplementedError  # TODO


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh CronScheduler (no lease store) from SCHEDULE/PAUSE/RESUME/TICK lines."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same driver as part1 -- the pause-vs-claim atomicity guarantee is exercised directly
    against CronScheduler with real threads in test_od05.py."""
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    """Same driver as part1, but the scheduler is constructed with a fresh LeaseStore -- a
    single-instance sanity check that passing a lease_store doesn't change behaviour. The
    multi-instance no-double-fire guarantee is exercised directly with two CronScheduler
    instances sharing one LeaseStore and real threads in test_od05.py."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
