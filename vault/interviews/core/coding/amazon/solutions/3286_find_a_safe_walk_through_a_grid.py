"""LC 3286 Find a Safe Walk Through a Grid -- 0-1 BFS: stepping on an unsafe cell costs 1, safe cell costs 0; need cost < health."""
from collections import deque
from random import Random

# --- solution ---
def find_safe_walk(grid, health):
    m, n = len(grid), len(grid[0])
    INF = float("inf")
    cost = [[INF] * n for _ in range(m)]
    cost[0][0] = grid[0][0]                               # the start cell also costs health if unsafe
    dq = deque([(0, 0)])
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                w = grid[nr][nc]
                if cost[r][c] + w < cost[nr][nc]:
                    cost[nr][nc] = cost[r][c] + w
                    if w == 0:
                        dq.appendleft((nr, nc))           # free edge: front of the deque keeps costs sorted
                    else:
                        dq.append((nr, nc))
    return cost[m - 1][n - 1] < health                    # health must stay >= 1 on arrival
# --- end ---

def _brute(grid, health):
    m, n = len(grid), len(grid[0])
    best = {(r, c): 10**9 for r in range(m) for c in range(n)}
    best[(0, 0)] = grid[0][0]
    changed = True
    while changed:                                        # Bellman-Ford style relaxation until stable
        changed = False
        for (r, c), v in list(best.items()):
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (r + dr, c + dc)
                if nb in best and v + grid[nb[0]][nb[1]] < best[nb]:
                    best[nb] = v + grid[nb[0]][nb[1]]
                    changed = True
    return best[(m - 1, n - 1)] < health

if __name__ == "__main__":
    assert find_safe_walk([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 1) is True
    assert find_safe_walk([[0, 1, 1, 0, 0, 0], [1, 0, 1, 0, 0, 0], [0, 1, 1, 1, 0, 1], [0, 0, 1, 0, 1, 0]], 3) is False
    assert find_safe_walk([[1, 1, 1], [1, 0, 1], [1, 1, 1]], 5) is True
    rng = Random(3286)
    for _ in range(500):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        if m * n < 2:
            continue
        g = [[1 if rng.random() < 0.4 else 0 for _ in range(n)] for _ in range(m)]
        h = rng.randint(1, m + n)
        assert find_safe_walk(g, h) == _brute(g, h), (g, h)
    print("ok 3286_find_a_safe_walk_through_a_grid")
