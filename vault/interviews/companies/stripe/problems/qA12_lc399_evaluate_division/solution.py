"""qA12 LC 399 Evaluate Division — reference solution.

Part 1: adjacency with inverse edges, BFS per query multiplying weights. Part 2: weighted union-find
(weight[x] = x / parent[x]) with path compression that re-multiplies weights. Part 3: DFS over simple
paths keeping the max product (quotes may disagree). Part 4: union-find again, flagging an equation
whose implied ratio differs from the given one by more than a relative tolerance.
"""
from __future__ import annotations

import sys
from collections import deque
from typing import NamedTuple


class Conflict(NamedTuple):
    index: int      # position in equations
    a: str
    b: str
    given: float    # values[index]
    implied: float  # ratio implied by the earlier (accepted) equations


def _adjacency(equations, values) -> dict[str, dict[str, float]]:
    adj: dict[str, dict[str, float]] = {}
    for (a, b), v in zip(equations, values):
        adj.setdefault(a, {})[b] = v
        adj.setdefault(b, {})[a] = 1.0 / v  # inverse edge
    return adj


def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    """Part 1 (LC signature): BFS with inverse edges; -1.0 when underivable."""
    adj = _adjacency(equations, values)
    out = []
    for src, dst in queries:
        if src not in adj or dst not in adj:
            out.append(-1.0)  # unknown variable, even for x/x
            continue
        seen = {src: 1.0}
        queue = deque([src])
        while queue and dst not in seen:
            cur = queue.popleft()
            for nxt, w in adj[cur].items():
                if nxt not in seen:
                    seen[nxt] = seen[cur] * w
                    queue.append(nxt)
        out.append(seen.get(dst, -1.0))  # src == dst -> 1.0 via the seed
    return out


class _WeightedUF:
    """parent[x], weight[x] = x / parent[x]."""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}
        self.weight: dict[str, float] = {}

    def add(self, x: str) -> None:
        if x not in self.parent:
            self.parent[x], self.weight[x] = x, 1.0

    def find(self, x: str) -> tuple[str, float]:
        """(root, x / root) with path compression — the weight must be re-multiplied on compression."""
        if self.parent[x] == x:
            return x, 1.0
        root, w = self.find(self.parent[x])
        self.parent[x], self.weight[x] = root, self.weight[x] * w
        return root, self.weight[x]

    def ratio(self, a: str, b: str) -> float | None:
        """a / b if connected, else None."""
        if a not in self.parent or b not in self.parent:
            return None
        ra, wa = self.find(a)
        rb, wb = self.find(b)
        return wa / wb if ra == rb else None

    def union(self, a: str, b: str, v: float) -> None:
        """Apply a / b = v (callers check consistency first when they care)."""
        self.add(a)
        self.add(b)
        ra, wa = self.find(a)
        rb, wb = self.find(b)
        if ra != rb:
            self.parent[ra] = rb
            self.weight[ra] = v * wb / wa  # ra/rb = (a/wa)/(b/wb) = v * wb / wa


def calc_equation_union_find(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    """Part 2: weighted union-find with path compression; same answers as Part 1."""
    uf = _WeightedUF()
    for (a, b), v in zip(equations, values):
        uf.union(a, b, v)
    return [r if (r := uf.ratio(s, d)) is not None else -1.0 for s, d in queries]


def best_rate_path(equations: list[list[str]], values: list[float], src: str, dst: str) -> tuple[float, list[str]] | None:
    """Part 3: max product over simple paths (inverse edges included); ties fewer hops, then lexicographic."""
    adj = _adjacency(equations, values)
    if src not in adj or dst not in adj:
        return None
    best: tuple[float, list[str]] | None = None
    path = [src]
    on_path = {src}

    def dfs(cur: str, product: float) -> None:
        nonlocal best
        if cur == dst:
            # better rate wins; equal rate -> fewer hops; equal hops -> the first found, which is the
            # lexicographically smaller path because neighbours are visited in sorted order (strict >)
            if best is None or (product, -len(path)) > (best[0], -len(best[1])):
                best = (product, path[:])
            return
        for nxt in sorted(adj[cur]):  # sorted -> lexicographically smaller paths are found first
            if nxt not in on_path:  # simple paths only: a bad quote cannot be looped
                on_path.add(nxt)
                path.append(nxt)
                dfs(nxt, product * adj[cur][nxt])
                path.pop()
                on_path.discard(nxt)

    dfs(src, 1.0)
    return best


def find_conflicts(equations: list[list[str]], values: list[float], rel_tol: float = 1e-9) -> list[Conflict]:
    """Part 4: equations that contradict the accepted ones before them (relative tolerance); not applied."""
    uf = _WeightedUF()
    conflicts = []
    for i, ((a, b), v) in enumerate(zip(equations, values)):
        uf.add(a)
        uf.add(b)  # register first so x/x = v is checked against the implied 1.0
        implied = uf.ratio(a, b)
        if implied is not None and abs(implied - v) > rel_tol * v:  # relative tolerance, strict >
            conflicts.append(Conflict(i, a, b, v, implied))
            continue  # earlier quotes win: the conflicting equation is not applied
        uf.union(a, b, v)
    return conflicts


def _parse_equation(text: str) -> tuple[str, str, float]:
    lhs, v = text.split("=")
    a, b = lhs.split("/")
    return a.strip(), b.strip(), float(v)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    sep = lines.index("?") if "?" in lines else len(lines)
    parsed = [_parse_equation(ln) for ln in lines[1:sep]]
    equations = [[a, b] for a, b, _ in parsed]
    values = [v for _, _, v in parsed]
    tail = lines[sep + 1:]
    if part in (1, 2):
        queries = [[p.strip() for p in ln.split("/")] for ln in tail]
        fn = calc_equation if part == 1 else calc_equation_union_find
        out = [f"{x:.5f}" for x in fn(equations, values, queries)]
    elif part == 3:
        src, dst = tail[0].split()
        r = best_rate_path(equations, values, src, dst)
        out = ["N/A" if r is None else f"{r[0]:.5f} " + " -> ".join(r[1])]
    else:
        conflicts = find_conflicts(equations, values)
        out = [f"{c.index}: {c.a}/{c.b} given={c.given:.5f} implied={c.implied:.5f}" for c in conflicts] or ["consistent"]
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
