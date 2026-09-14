"""qA11 LC 2768 Number of Black Blocks — reference solution.

Iterate the black cells, not the grid: each cell touches <= k*k blocks (top-left corners in range),
count those in a dict, and get bucket 0 by subtraction from the total number of blocks. Part 3 keeps
the same dict plus the histogram and moves blocks between buckets on every paint.
"""
from __future__ import annotations

import sys


def _touched(m: int, n: int, coordinates, k: int) -> dict[tuple[int, int], int]:
    """Black-cell count per touched k x k block (keyed by top-left corner)."""
    per_block: dict[tuple[int, int], int] = {}
    for x, y in set(map(tuple, coordinates)):  # dedupe: a repeated coordinate is one black cell
        for dx in range(k):
            bx = x - dx
            if bx < 0 or bx > m - k:  # top-left row must keep the block inside the grid
                continue
            for dy in range(k):
                by = y - dy
                if 0 <= by <= n - k:
                    per_block[(bx, by)] = per_block.get((bx, by), 0) + 1
    return per_block


def count_black_blocks_k(m: int, n: int, coordinates: list[list[int]], k: int) -> list[int]:
    """Part 2: k*k+1 counts for k x k blocks (k == 2 is Part 1)."""
    per_block = _touched(m, n, coordinates, k)
    result = [0] * (k * k + 1)
    for c in per_block.values():
        result[c] += 1
    # bucket 0 by arithmetic: the grid is never materialised (m*n can be 10^10)
    result[0] = max(0, m - k + 1) * max(0, n - k + 1) - len(per_block)
    return result


def count_black_blocks(m: int, n: int, coordinates: list[list[int]]) -> list[int]:
    """Part 1 (LC signature): five counts, result[i] = number of 2x2 blocks with exactly i black cells."""
    return count_black_blocks_k(m, n, coordinates, 2)


class BlockCounter:
    """Part 3: streaming paints with an always-ready histogram of 2x2 block counts."""

    def __init__(self, m: int, n: int) -> None:
        self.m, self.n = m, n
        self.black: set[tuple[int, int]] = set()
        self.per_block: dict[tuple[int, int], int] = {}  # only blocks with count >= 1
        self.hist = [0] * 5  # hist[c] for c >= 1; hist[0] is derived in counts()

    def _blocks(self, x: int, y: int):
        for bx in (x - 1, x):
            if 0 <= bx <= self.m - 2:
                for by in (y - 1, y):
                    if 0 <= by <= self.n - 2:
                        yield bx, by

    def paint(self, x: int, y: int, black: bool) -> None:
        """Set the cell colour (idempotent); O(1)."""
        cell = (x, y)
        if black == (cell in self.black):
            return  # no change -> nothing moves between buckets
        delta = 1 if black else -1
        (self.black.add if black else self.black.discard)(cell)
        for b in self._blocks(x, y):
            c = self.per_block.get(b, 0)
            self.hist[c] -= 1
            c += delta
            self.hist[c] += 1
            if c:
                self.per_block[b] = c
            else:
                del self.per_block[b]  # back to zero black cells -> counted in bucket 0 by subtraction

    def counts(self) -> list[int]:
        """Five counts as in Part 1; O(1)."""
        out = self.hist[:]
        out[0] = (self.m - 1) * (self.n - 1) - len(self.per_block)
        return out


def _xy(text: str) -> tuple[int, int]:
    a, b = text.split(",")
    return int(a), int(b)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    m, n = (int(v) for v in lines[1].split())
    k, rest = 2, lines[2:]
    if rest and rest[0].upper().startswith("K "):
        k, rest = int(rest[0].split()[1]), rest[1:]
    out: list[str] = []
    if part in (1, 2):
        coords = [list(_xy(ln)) for ln in rest]
        counts = count_black_blocks(m, n, coords) if part == 1 else count_black_blocks_k(m, n, coords, k)
        out.append(" ".join(map(str, counts)))
    else:
        bc = BlockCounter(m, n)
        for ln in rest:
            op = ln[0].upper()
            if op == "Q":
                out.append(" ".join(map(str, bc.counts())))
            else:
                x, y = _xy(ln[1:])
                bc.paint(x, y, op == "B")
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
