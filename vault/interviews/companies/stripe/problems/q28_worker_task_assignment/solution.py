"""q28 Worker Task Assignment — reference solution.

One engine, three switches (skills / specialist / capacity). Per skill a min-heap of
(load, n_skills_or_0, worker_id, version): a worker's load change bumps its version and pushes a
fresh entry into each of its skill heaps; stale entries are skipped when popped (lazy
invalidation). Candidates that do not fit the capacity are popped, parked, and pushed back after
the choice (worst case O(W log W) for a task nobody fits; typical O(k log W)).
A plain O(W) scan per task (`min(workers, key=...)`) is the 35-minute version; it is ~10^8
comparisons on the 10^5 x 10^3 perf test, which is why the heaps exist.
"""
from __future__ import annotations

import heapq
import sys
from collections import defaultdict

ANY = "*"   # pseudo-skill used when skills are ignored (Part 1)


class Worker:
    __slots__ = ("id", "skills", "capacity", "load", "ver")

    def __init__(self, wid: str, skills: list[str], capacity: int) -> None:
        self.id, self.skills, self.capacity = wid, sorted(set(skills)), capacity   # duplicates count once
        self.load, self.ver = 0, 0


def parse(lines: list[str]) -> tuple[list[Worker], list[tuple[str, str, int]]]:
    workers, tasks, section = [], [], None
    for raw in lines:
        ln = raw.strip()
        if not ln:
            continue
        if ln.upper() in ("WORKERS", "TASKS"):
            section = ln.upper()
            continue
        f = [p.strip() for p in ln.split(",")]
        if section == "WORKERS":
            workers.append(Worker(f[0], [s.strip() for s in f[1].split(";") if s.strip()], int(f[2])))
        else:
            tasks.append((f[0], f[1], int(f[2])))
    return workers, tasks


def assign(lines: list[str], use_skills: bool, specialist: bool, use_capacity: bool) -> list[str]:
    workers, tasks = parse(lines)
    heaps: dict[str, list[tuple[int, int, str, int]]] = defaultdict(list)

    def key(w: Worker) -> tuple[int, int, str, int]:
        # tie-break: load, then (Part 3) fewer skills, then id (plain string order)
        return (w.load, len(w.skills) if specialist else 0, w.id, w.ver)

    def push(w: Worker) -> None:
        for s in (w.skills if use_skills else [ANY]):
            heapq.heappush(heaps[s], key(w))

    by_id = {w.id: w for w in workers}
    for w in workers:
        push(w)

    out = []
    for tid, skill, cost in tasks:
        heap = heaps.get(skill if use_skills else ANY, [])
        parked, chosen = [], None
        while heap:
            entry = heapq.heappop(heap)
            w = by_id[entry[2]]
            if entry[3] != w.ver:                       # stale: the worker's load changed since
                continue
            if use_capacity and w.load + cost > w.capacity:   # must fit: load + cost <= capacity
                parked.append(entry)
                continue
            chosen = w
            break
        for entry in parked:                            # non-fitting workers stay in the pool
            heapq.heappush(heap, entry)
        if chosen is None:
            out.append(f"{tid} -> UNASSIGNED")
            continue
        chosen.load += cost
        chosen.ver += 1
        push(chosen)                                    # fresh entries; old ones are now stale
        out.append(f"{tid} -> {chosen.id}")
    out.extend(f"{w.id} {w.load}" for w in sorted(workers, key=lambda w: w.id))
    return out


def part1(lines: list[str]) -> list[str]:
    return assign(lines, use_skills=False, specialist=False, use_capacity=False)


def part2(lines: list[str]) -> list[str]:
    return assign(lines, use_skills=True, specialist=False, use_capacity=False)


def part3(lines: list[str]) -> list[str]:
    return assign(lines, use_skills=True, specialist=True, use_capacity=False)


def part4(lines: list[str]) -> list[str]:
    return assign(lines, use_skills=True, specialist=True, use_capacity=True)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 4
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
