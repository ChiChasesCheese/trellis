"""q15 Graph Valid Tree -- reference solution.

Part 1 is LC 261 "Graph Valid Tree" verbatim: given `n` nodes labeled 0..n-1 and a
list of undirected `edges`, determine whether they form a valid tree -- i.e. the
graph is connected AND acyclic. A tree on n nodes has exactly n-1 edges; that's a
necessary but not sufficient condition (e.g. two disjoint components can also
happen to not have n-1 edges only if disconnected, but a graph could have n-1
edges and still contain a cycle if it's disconnected elsewhere), so it's checked
alongside union-find (or BFS/DFS) rather than relied on alone.

Part 2 (reconstructed): edges arrive one at a time; after each edge is added,
report whether the graph built so far is still acyclic (a "forest"), and how many
connected components remain. This is the natural online counterpart of Part 1 --
union-find with path compression + union by size gives O(alpha(n)) per edge.
"""
from __future__ import annotations

import sys


def _validate(n: int, edges: list[list[int]]) -> None:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError(f"n must be a positive int: {n!r}")
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError(f"edge must be [u, v]: {e!r}")
        u, v = e
        if not isinstance(u, int) or not isinstance(v, int) or isinstance(u, bool) or isinstance(v, bool):
            raise ValueError(f"edge endpoints must be int: {e!r}")
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"edge endpoint out of range [0, {n}): {e!r}")
        if u == v:
            raise ValueError(f"self-loop is not a valid edge: {e!r}")


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Returns True if a and b were merged (previously separate), False if
        they were already in the same component (this edge would create a cycle)."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


# --------------------------------------------------------------------------- Part 1
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """LC261: n nodes, undirected edges -> True iff they form a valid tree."""
    _validate(n, edges)
    if len(edges) != n - 1:
        return False
    uf = _UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return False  # cycle
    return uf.components == 1  # redundant given len==n-1 and no cycle, but explicit


# --------------------------------------------------------------------------- Part 2
def valid_tree_online(n: int, edges: list[list[int]]) -> list[tuple[bool, int]]:
    """For each edge added in order, report (still_acyclic, components_remaining)
    after that edge. Once still_acyclic is False it stays False for every
    subsequent edge (a cycle, once introduced, never disappears by adding more
    edges); components_remaining keeps decreasing only while merges happen."""
    _validate(n, edges)
    uf = _UnionFind(n)
    acyclic_so_far = True
    out: list[tuple[bool, int]] = []
    for u, v in edges:
        if not uf.union(u, v):
            acyclic_so_far = False
        out.append((acyclic_so_far, uf.components))
    return out


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str]) -> tuple[int, list[list[int]]]:
    n, m = map(int, lines[0].split())
    edges = [list(map(int, lines[1 + i].split())) for i in range(m)]
    return n, edges


def part1(lines: list[str]) -> list[str]:
    """'n m' / m lines 'u v' -> ['true' / 'false']."""
    n, edges = _read(lines)
    return ["true" if valid_tree(n, edges) else "false"]


def part2(lines: list[str]) -> list[str]:
    """same input -> one line per edge: 'true|false components'."""
    n, edges = _read(lines)
    return [f"{'true' if ok else 'false'} {comp}" for ok, comp in valid_tree_online(n, edges)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
