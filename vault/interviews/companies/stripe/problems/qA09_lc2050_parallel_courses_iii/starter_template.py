"""qA09 LC 2050 Parallel Courses III — YOUR implementation. Run: python drill.py test qA09"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Slot(NamedTuple):
    job: int    # 1-based
    start: int
    end: int


def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    """Part 1 (LC signature): months until every job is done with unlimited parallelism."""
    # TODO
    return 0


def critical_path(n: int, relations: list[list[int]], time: list[int]) -> list[int]:
    """Part 2: one longest chain of jobs (1-based ids, execution order); ties -> smallest id."""
    # TODO
    return []


def schedule_k_workers(n: int, relations: list[list[int]], time: list[int], k: int) -> list[Slot]:
    """Part 3: list scheduling with at most k concurrent jobs, priority = longest tail then smallest id."""
    # TODO
    return []


def makespan_k_workers(n: int, relations: list[list[int]], time: list[int], k: int) -> int:
    """Part 3: max(end) of schedule_k_workers, 0 when n == 0."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    # TODO: PART n / [K k] / n / durations / prev,next lines
    stdout.write("")


if __name__ == "__main__":
    main()
