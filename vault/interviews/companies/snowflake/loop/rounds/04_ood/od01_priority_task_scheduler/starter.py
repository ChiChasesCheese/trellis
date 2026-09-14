"""od01 Priority Task Scheduler -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: tie-break order, duplicate-ID suppression, the
concurrency invariant, and the snapshot()/replay() persistence contract.
"""

from __future__ import annotations

import sys


class TaskScheduler:
    def __init__(self) -> None:
        pass  # TODO: pending entries, executed set, a lock, and an operation log

    def add(self, task_id: str, priority: int, timestamp: int) -> None:
        """No-op if task_id was already executed. Otherwise (re-)register it, replacing any
        earlier un-executed (priority, timestamp) for the same task_id."""
        raise NotImplementedError  # TODO

    def execute(self) -> str:
        """Pop the highest-priority eligible task: priority desc, then timestamp asc, then
        task_id asc (lexicographic). '' if nothing eligible. Must be atomic under concurrency:
        two concurrent execute() calls never both return the same task_id."""
        raise NotImplementedError  # TODO

    def snapshot(self) -> list[str]:
        """Return the op log (one 'ADD id p t' / 'EXEC' string per call) since construction."""
        raise NotImplementedError  # TODO

    @classmethod
    def replay(cls, log: list[str]) -> "TaskScheduler":
        """Rebuild a scheduler from scratch by re-applying a snapshot()'d log."""
        raise NotImplementedError  # TODO


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh TaskScheduler from ADD/EXEC lines; return one output string per EXEC."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same driver as part1 -- duplicate-ID suppression is a property of TaskScheduler itself,
    exercised here with task_id values that repeat."""
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    """Same driver as part1, single-threaded (the concurrency guarantee is exercised directly
    against TaskScheduler with real threads in test_od01.py, not through this line-oriented
    driver)."""
    return part1(lines)


def part4(lines: list[str]) -> list[str]:
    """Like part1, but a `SNAPSHOT` line swaps the live scheduler for
    TaskScheduler.replay(current.snapshot()) and all following lines run against the rebuilt
    instance. Correct snapshot()/replay() makes this swap invisible in the output."""
    # TODO
    return []


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
