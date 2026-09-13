"""qA09 LC 2050 Parallel Courses III — reference solution.

Part 1 is Kahn's algorithm carrying `finish[j] = time[j] + max finish of prerequisites`. Part 2 keeps
the arg-max predecessor and walks back from the latest finisher. Part 3 is list scheduling: longest
tail (Part 1 on the reversed graph) first, event-driven simulation with a heap of running jobs.
Everything is iterative — a 5*10^4 chain would blow the recursion limit.
"""
from __future__ import annotations

import heapq
import sys
from collections import deque
from typing import NamedTuple


class Slot(NamedTuple):
    job: int    # 1-based
    start: int
    end: int


def _graph(n: int, relations: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    """0-based adjacency (prev -> next) and indegrees."""
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for prev, nxt in relations:  # relations are 1-based, time[] is 0-based
        succ[prev - 1].append(nxt - 1)
        indeg[nxt - 1] += 1
    return succ, indeg


def _topo(n: int, succ: list[list[int]], indeg: list[int]) -> list[int]:
    """Kahn's order, smallest-id-first among simultaneously ready jobs (deterministic)."""
    indeg = indeg[:]
    queue = deque(j for j in range(n) if indeg[j] == 0)
    order: list[int] = []
    while queue:
        j = queue.popleft()
        order.append(j)
        for s in succ[j]:
            indeg[s] -= 1
            if indeg[s] == 0:
                queue.append(s)
    return order


def _finish_and_pred(n: int, relations: list[list[int]], time: list[int]) -> tuple[list[int], list[int]]:
    """finish[j] = time[j] + max finish over prerequisites; pred[j] = that arg-max (smallest id on ties, -1 if none)."""
    succ, indeg = _graph(n, relations)
    finish = time[:]  # no prerequisites -> finish == own duration
    pred = [-1] * n
    for j in _topo(n, succ, indeg):  # every predecessor of s is final when s is popped
        for s in succ[j]:
            cand = finish[j] + time[s]
            # strict >: an earlier (smaller-id) predecessor with an equal finish is kept
            if cand > finish[s] or (cand == finish[s] and pred[s] != -1 and j < pred[s]):
                finish[s], pred[s] = cand, j
    return finish, pred


def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    """Part 1 (LC signature): months until every job is done with unlimited parallelism."""
    finish, _ = _finish_and_pred(n, relations, time)
    return max(finish, default=0)


def critical_path(n: int, relations: list[list[int]], time: list[int]) -> list[int]:
    """Part 2: one longest chain of jobs (1-based ids, execution order); ties -> smallest id."""
    finish, pred = _finish_and_pred(n, relations, time)
    if n == 0:
        return []
    end = max(range(n), key=lambda j: (finish[j], -j))  # largest finish, smallest id on ties
    path = []
    while end != -1:
        path.append(end + 1)
        end = pred[end]
    return path[::-1]


def schedule_k_workers(n: int, relations: list[list[int]], time: list[int], k: int) -> list[Slot]:
    """Part 3: list scheduling with at most k concurrent jobs, priority = longest tail then smallest id."""
    succ, indeg = _graph(n, relations)
    order = _topo(n, succ, indeg)
    tail = time[:]  # longest chain from j to a sink, computed in reverse topological order
    for j in reversed(order):
        for s in succ[j]:
            tail[j] = max(tail[j], time[j] + tail[s])
    ready = [(-tail[j], j) for j in range(n) if indeg[j] == 0]  # heap: longest tail, then smallest id
    heapq.heapify(ready)
    running: list[tuple[int, int]] = []  # (end, job)
    slots: list[Slot] = []
    now = 0
    while ready or running:
        while ready and len(running) < k:  # fill free workers greedily, never pre-empt
            _, j = heapq.heappop(ready)
            heapq.heappush(running, (now + time[j], j))
            slots.append(Slot(j + 1, now, now + time[j]))
        now = running[0][0]  # jump to the earliest end; retire everything ending then
        while running and running[0][0] == now:
            _, j = heapq.heappop(running)
            for s in succ[j]:
                indeg[s] -= 1
                if indeg[s] == 0:
                    heapq.heappush(ready, (-tail[s], s))
    slots.sort(key=lambda s: (s.start, s.job))
    return slots


def makespan_k_workers(n: int, relations: list[list[int]], time: list[int], k: int) -> int:
    """Part 3: max(end) of schedule_k_workers, 0 when n == 0."""
    return max((s.end for s in schedule_k_workers(n, relations, time, k)), default=0)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    k, rest = 0, lines[1:]
    if rest and rest[0].upper().startswith("K "):
        k, rest = int(rest[0].split()[1]), rest[1:]
    n = int(rest[0])
    time = [int(x) for x in rest[1].split()] if n else []
    relations = [[int(x) for x in ln.split(",")] for ln in rest[2:] if n]
    if part == 1:
        out = [str(minimum_time(n, relations, time))]
    elif part == 2:
        path = critical_path(n, relations, time)
        out = [" -> ".join(map(str, path)), str(sum(time[j - 1] for j in path))]
    else:
        slots = schedule_k_workers(n, relations, time, k)
        out = [str(max((s.end for s in slots), default=0))] + [f"{s.job} {s.start} {s.end}" for s in slots]
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
