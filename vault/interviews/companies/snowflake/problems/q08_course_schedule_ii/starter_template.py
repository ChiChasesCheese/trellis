"""q08 Course Schedule II — YOUR implementation. Run: python drill.py test q08"""
from __future__ import annotations

import sys


def part1(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """LC210 convention: prerequisites[i] = [a, b] means a requires b (0-indexed
    courses 0..num_courses-1). Ties among ready courses are broken by SMALLEST
    course id first (min-heap). Returns [] if there is a cycle."""
    # TODO
    return []


def part2(num_courses: int, relations: list[list[int]]) -> int:
    """LC1136 convention: courses labeled 1..num_courses, relations[i] = [a, b]
    means a must be completed before b (edge a -> b). Returns the minimum number
    of semesters (BFS layers) to complete all courses, or -1 if there is a cycle."""
    # TODO
    return 0


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
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
