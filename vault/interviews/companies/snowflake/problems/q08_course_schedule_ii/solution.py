"""q08 Course Schedule II — reference solution.

Part 1 is LC 210 "Course Schedule II" verbatim: courses labeled 0..num_courses-1,
prerequisites[i] = [a, b] means "a requires b" (b must be taken before a). Kahn's
algorithm topological sort, but the ready set (in-degree 0 courses) is a MIN-HEAP
so that among all currently available courses the smallest course id is always
processed next -> deterministic output. Return [] if there is a cycle.

Part 2 is a from-scratch "minimum parallel semesters" follow-up, formalized after
the LC 1136 "Parallel Courses" shape referenced in the catalog. To keep faith with
LC1136's own convention (not LC210's), courses here are labeled 1..num_courses and
relations[i] = [a, b] means "a must be completed before b" (a -> b edge). Each
semester you may take any number of courses in parallel as long as every
prerequisite was completed in a STRICTLY EARLIER semester; this is exactly the
number of BFS layers (Kahn's algorithm processed level-by-level) needed to drain
the whole DAG. Return -1 if a cycle prevents finishing all courses.
"""
from __future__ import annotations

import heapq
import sys
from collections import deque


def part1(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """LC210 convention: prerequisites[i] = [a, b] means a requires b (0-indexed
    courses 0..num_courses-1). Ties among ready courses are broken by SMALLEST
    course id first (min-heap). Returns [] if there is a cycle."""
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1

    heap = [c for c in range(num_courses) if indeg[c] == 0]
    heapq.heapify(heap)
    order: list[int] = []
    while heap:
        course = heapq.heappop(heap)
        order.append(course)
        for nxt in adj[course]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    return order if len(order) == num_courses else []


def part2(num_courses: int, relations: list[list[int]]) -> int:
    """LC1136 convention: courses labeled 1..num_courses, relations[i] = [a, b]
    means a must be completed before b (edge a -> b). Returns the minimum number
    of semesters (BFS layers) to complete all courses, or -1 if there is a cycle."""
    adj: list[list[int]] = [[] for _ in range(num_courses + 1)]
    indeg = [0] * (num_courses + 1)
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1

    queue = deque(c for c in range(1, num_courses + 1) if indeg[c] == 0)
    taken = 0
    semesters = 0
    while queue:
        semesters += 1
        for _ in range(len(queue)):
            course = queue.popleft()
            taken += 1
            for nxt in adj[course]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
    return semesters if taken == num_courses else -1


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format:
    PART 1
    num_courses
    num_prerequisites
    a b            (repeated num_prerequisites times; prerequisites[i] = [a, b])

    PART 2
    num_courses
    num_relations
    a b            (repeated num_relations times; relations[i] = [a, b])

    Output for PART 1: the order as space-separated ints on one line (blank line
    if impossible). Output for PART 2: a single integer (-1 if impossible).
    """
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header and header[0].upper() == "PART" else 1
    num_courses = int(lines[idx])
    idx += 1
    num_edges = int(lines[idx])
    idx += 1
    edges: list[list[int]] = []
    for _ in range(num_edges):
        a, b = lines[idx].split()
        idx += 1
        edges.append([int(a), int(b)])

    if part == 1:
        order = part1(num_courses, edges)
        stdout.write(" ".join(str(c) for c in order) + "\n")
    else:
        stdout.write(f"{part2(num_courses, edges)}\n")


if __name__ == "__main__":
    main()
