"""od05 Cron Scheduler -- reference solution.

The cron matcher converts `now` (minutes since epoch) to UTC calendar fields once per tick and
checks each of the 5 fields independently ('*' / '*/n' / a fixed integer). CronScheduler keeps a
lock around its own job/pause bookkeeping; claiming a (job_id, minute) is delegated to a shared
LeaseStore when one is supplied (Part3's multi-instance case) or to a local claim set otherwise
(Part1/Part2, single instance). Either way "is this job still unpaused" is re-checked right
before the claim attempt, closing the pause-vs-claim race window as tightly as a single process
can without a distributed transaction.
"""

from __future__ import annotations

import sys
import threading
from datetime import datetime, timezone


def _field_match(field: str, value: int) -> bool:
    if field == "*":
        return True
    if field.startswith("*/"):
        return value % int(field[2:]) == 0
    return int(field) == value


def _matches(cron_expr: str, now: int) -> bool:
    minute_f, hour_f, day_f, month_f, weekday_f = cron_expr.split()
    dt = datetime.fromtimestamp(now * 60, tz=timezone.utc)
    return (
        _field_match(minute_f, dt.minute)
        and _field_match(hour_f, dt.hour)
        and _field_match(day_f, dt.day)
        and _field_match(month_f, dt.month)
        and _field_match(weekday_f, dt.weekday())
    )


class LeaseStore:
    def __init__(self) -> None:
        self._claimed: set[tuple[str, int]] = set()
        self._lock = threading.Lock()

    def try_claim(self, job_id: str, minute: int) -> bool:
        with self._lock:
            key = (job_id, minute)
            if key in self._claimed:
                return False
            self._claimed.add(key)
            return True


class CronScheduler:
    def __init__(self, lease_store: "LeaseStore | None" = None) -> None:
        self._jobs: dict[str, str] = {}
        self._paused: set[str] = set()
        self._lease_store = lease_store
        self._local_claims: set[tuple[str, int]] = set()
        self._lock = threading.Lock()

    def schedule(self, job_id: str, cron_expr: str) -> None:
        with self._lock:
            self._jobs[job_id] = cron_expr
            self._paused.discard(job_id)

    def pause(self, job_id: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._paused.add(job_id)

    def resume(self, job_id: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._paused.discard(job_id)

    def tick(self, now: int) -> list[str]:
        with self._lock:
            snapshot = [
                (job_id, expr) for job_id, expr in self._jobs.items() if job_id not in self._paused
            ]

        fired = []
        for job_id, expr in snapshot:
            if not _matches(expr, now):
                continue
            if self._claim(job_id, now):
                fired.append(job_id)
        return fired

    def _claim(self, job_id: str, minute: int) -> bool:
        if self._lease_store is not None:
            return self._lease_store.try_claim(job_id, minute)
        with self._lock:
            if job_id in self._paused:
                return False  # re-check right before claiming: closes most of the race window
            key = (job_id, minute)
            if key in self._local_claims:
                return False
            self._local_claims.add(key)
            return True


# ---------------------------------------------------------------------- line-driven wrappers
def _run(scheduler: CronScheduler, lines: list[str]) -> list[str]:
    out: list[str] = []
    for raw in lines:
        fields = raw.split()
        verb = fields[0]
        if verb == "SCHEDULE":
            scheduler.schedule(fields[1], " ".join(fields[2:]))
        elif verb == "PAUSE":
            scheduler.pause(fields[1])
        elif verb == "RESUME":
            scheduler.resume(fields[1])
        elif verb == "TICK":
            out.append(repr(sorted(scheduler.tick(int(fields[1])))))
        else:
            raise ValueError(f"bad line: {raw!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _run(CronScheduler(), lines)


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    return _run(CronScheduler(lease_store=LeaseStore()), lines)


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
