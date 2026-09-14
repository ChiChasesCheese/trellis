"""od01 Priority Task Scheduler -- reference solution.

One dict of currently-pending (priority, timestamp) per task_id, a set of executed ids, and a
lazily-cleaned heap keyed for the tie-break order (priority desc, timestamp asc, task_id asc).
Re-adding a not-yet-executed task_id bumps a per-id version counter so the old heap entry can be
recognised as stale and skipped instead of physically removed (no O(n) heap search on re-add).
A single lock guards the whole "scan candidates -> mark executed" critical section so concurrent
execute() calls never both return the same id. snapshot()/replay() persist by operation log, not
by serializing the heap -- replaying the log from empty state reconstructs an equivalent
scheduler (same future add/execute behaviour), which is the contract problem.md commits to.
"""

from __future__ import annotations

import heapq
import sys
import threading


class TaskScheduler:
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str, int]] = []  # (-priority, ts, task_id, version)
        self._versions: dict[str, int] = {}
        self._executed: set[str] = set()
        self._log: list[str] = []
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- public API
    def add(self, task_id: str, priority: int, timestamp: int) -> None:
        with self._lock:
            self._log.append(f"ADD {task_id} {priority} {timestamp}")
            self._add_locked(task_id, priority, timestamp)

    def execute(self) -> str:
        with self._lock:
            result = self._execute_locked()
            self._log.append("EXEC")
            return result

    def snapshot(self) -> list[str]:
        with self._lock:
            return list(self._log)

    @classmethod
    def replay(cls, log: list[str]) -> "TaskScheduler":
        sched = cls()
        for line in log:
            line = line.strip()
            if not line:
                continue
            if line == "EXEC":
                sched.execute()
            else:
                _, task_id, priority, timestamp = line.split()
                sched.add(task_id, int(priority), int(timestamp))
        return sched

    # ---------------------------------------------------------------- internals (lock held)
    def _add_locked(self, task_id: str, priority: int, timestamp: int) -> None:
        if task_id in self._executed:
            return  # permanently ineligible; adding again is a no-op
        version = self._versions.get(task_id, 0) + 1
        self._versions[task_id] = version
        heapq.heappush(self._heap, (-priority, timestamp, task_id, version))

    def _execute_locked(self) -> str:
        while self._heap:
            neg_priority, timestamp, task_id, version = heapq.heappop(self._heap)
            if task_id in self._executed or self._versions.get(task_id) != version:
                continue  # stale (already executed, or superseded by a later add)
            self._executed.add(task_id)
            return task_id
        return ""


# ---------------------------------------------------------------------- line-driven wrappers
_ARITY = {"ADD": 3, "EXEC": 0, "SNAPSHOT": 0}


def part1(lines: list[str]) -> list[str]:
    sched = TaskScheduler()
    out: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        fields = line.split()
        verb = fields[0]
        if verb not in _ARITY or len(fields) - 1 != _ARITY[verb]:
            raise ValueError(f"bad line: {raw!r}")
        if verb == "ADD":
            sched.add(fields[1], int(fields[2]), int(fields[3]))
        elif verb == "EXEC":
            out.append(sched.execute())
        else:  # SNAPSHOT -- ignored outside part4, but harmless (see part4)
            sched = TaskScheduler.replay(sched.snapshot())
    return out


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    return part1(lines)


def part4(lines: list[str]) -> list[str]:
    return part1(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
