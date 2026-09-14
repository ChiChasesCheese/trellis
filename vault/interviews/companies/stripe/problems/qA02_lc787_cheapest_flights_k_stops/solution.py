"""qA02 LC 787 Cheapest Flights Within K Stops — reference solution.

Part 1: Bellman-Ford limited to k+1 rounds, each round relaxing from a COPY of the previous round
(the classic bug is relaxing in place, which lets one round chain several flights).
Part 2: the same layering expressed as a BFS frontier by hop count.
Part 3: layered DP that carries (cost, path) and breaks ties (fewer flights, lexicographic path).
Part 4: q22-style string routes with a carrier filter, mapped onto Part 1.
"""
from __future__ import annotations

import sys
from collections import defaultdict

INF = float("inf")


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """Part 1: k+1 rounds of edge relaxation; round r yields best cost using <= r flights."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        prev = dist[:]  # relax from the previous round only -> each round adds at most ONE flight
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return -1 if dist[dst] == INF else int(dist[dst])


def find_cheapest_price_bfs(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """Part 2: frontier by hops. A city is re-entered only if the new cost beats the best ever seen
    for it (an earlier visit with <= cost has fewer hops AND is cheaper, so it dominates)."""
    adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in flights:
        adj[u].append((v, w))
    best = [INF] * n
    best[src] = 0
    frontier = {src: 0}
    for _ in range(k + 1):
        nxt: dict[int, int] = {}
        for u, cost in frontier.items():
            for v, w in adj[u]:
                if cost + w < best[v]:  # strict: equal cost with more hops is never useful
                    best[v] = cost + w
                    nxt[v] = cost + w
        if not nxt:
            break
        frontier = nxt
    return -1 if best[dst] == INF else int(best[dst])


def cheapest_path(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> list[int] | None:
    """Part 3: same layering as Part 1, carrying the path; key = (cost, flights, path) so ties go to
    fewer flights, then the lexicographically smaller city list."""
    best: list[tuple[int, int, tuple[int, ...]] | None] = [None] * n
    best[src] = (0, 0, (src,))
    for _ in range(k + 1):
        prev = best[:]
        for u, v, w in flights:
            if prev[u] is None:
                continue
            cost, hops, path = prev[u]
            cand = (cost + w, hops + 1, path + (v,))
            if best[v] is None or cand < best[v]:
                best[v] = cand
    return None if best[dst] is None else list(best[dst][2])


def cheapest_with_carrier(routes: list[str], src: str, dst: str, k: int, carrier: str = "*") -> int:
    """Part 4: parse 'FROM:TO:CARRIER:price', keep the carrier's routes (or all for '*'), reuse Part 1."""
    ids: dict[str, int] = {}

    def cid(name: str) -> int:
        return ids.setdefault(name, len(ids))

    flights = []
    for r in routes:
        a, b, c, price = (p.strip() for p in r.split(":"))
        if carrier == "*" or c == carrier:
            flights.append([cid(a), cid(b), int(price)])
    if src not in ids or dst not in ids:
        return 0 if src == dst else -1
    return find_cheapest_price(len(ids), flights, ids[src], ids[dst], k)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    if part == 4:
        src, dst, k, carrier = lines[1].split()
        ans = cheapest_with_carrier(lines[2:], src, dst, int(k), carrier)
        stdout.write(f"{ans}\n")
        return
    n, src, dst, k = (int(x) for x in lines[1].split())
    flights = [[int(x) for x in ln.split()] for ln in lines[2:]]
    if part == 1:
        stdout.write(f"{find_cheapest_price(n, flights, src, dst, k)}\n")
    elif part == 2:
        stdout.write(f"{find_cheapest_price_bfs(n, flights, src, dst, k)}\n")
    else:
        path = cheapest_path(n, flights, src, dst, k)
        if path is None:
            stdout.write("-1\n")
        else:
            price = find_cheapest_price(n, flights, src, dst, k)
            stdout.write(" -> ".join(map(str, path)) + f" ({price})\n")


if __name__ == "__main__":
    main()
