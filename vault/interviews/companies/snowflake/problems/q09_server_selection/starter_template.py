"""q09 Server Selection with switching cost — YOUR implementation. Run: python drill.py test q09"""
from __future__ import annotations

import sys


def part1(m: int, n: int, cost: list[list[int]], switch_cost: int) -> int:
    """O(m^2 * n) baseline: for each slot/server, scan all other servers at the
    previous slot. Returns the minimum total cost."""
    # TODO
    return 0


def part2(m: int, n: int, cost: list[list[int]], switch_cost: int) -> tuple[int, list[int]]:
    """O(m*n): track best/second-best previous-slot total cost. Returns
    (min_total_cost, assignment) where assignment[i] is the server active at
    slot i achieving the minimum (see problem.md for the tie-break rules)."""
    # TODO
    return 0, []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header and header[0].upper() == "PART" else 2
    m, n, switch_cost = (int(x) for x in lines[idx].split())
    idx += 1
    cost: list[list[int]] = []
    for _ in range(m):
        row = [int(x) for x in lines[idx].split()] if n > 0 else []
        idx += 1 if n > 0 else 0
        cost.append(row)

    if part == 1:
        stdout.write(f"{part1(m, n, cost, switch_cost)}\n")
    else:
        total, assignment = part2(m, n, cost, switch_cost)
        stdout.write(f"{total}\n")
        stdout.write(" ".join(str(s) for s in assignment) + "\n")


if __name__ == "__main__":
    main()
