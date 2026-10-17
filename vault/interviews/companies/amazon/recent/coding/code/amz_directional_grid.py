"""Directional BFS (reconstructed): a step moves one cell; the new heading is straight or a left turn, never right / U-turn. State = (r, c, heading)."""
from collections import deque
from random import Random

# --- solution ---
HEADINGS = ((-1, 0), (0, 1), (1, 0), (0, -1))             # N E S W, so (h + 1) % 4 is a right turn and (h - 1) % 4 a left turn

def min_steps(grid, start, target):
    m, n = len(grid), len(grid[0])
    queue = deque((start[0], start[1], h, 0) for h in range(4))   # the first step may head anywhere
    seen = {(start[0], start[1], h) for h in range(4)}
    while queue:
        r, c, h, d = queue.popleft()
        if (r, c) == tuple(target):
            return d
        for nh in (h, (h - 1) % 4):                       # straight or left; right and reverse are simply not listed
            nr, nc = r + HEADINGS[nh][0], c + HEADINGS[nh][1]
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc, nh) not in seen:
                seen.add((nr, nc, nh))
                queue.append((nr, nc, nh, d + 1))
    return -1
# --- end ---

def _brute(grid, start, target, limit):
    m, n = len(grid), len(grid[0])
    best = [None]
    def go(r, c, h, d):                                   # exhaustive DFS over move sequences of length <= limit
        if (r, c) == tuple(target):
            best[0] = d if best[0] is None else min(best[0], d)
            return
        if d == limit:
            return
        for nh in range(4):
            if h is not None and nh in ((h + 1) % 4, (h + 2) % 4):
                continue
            nr, nc = r + HEADINGS[nh][0], c + HEADINGS[nh][1]
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0:
                go(nr, nc, nh, d + 1)
    go(start[0], start[1], None, 0)
    return -1 if best[0] is None else best[0]

if __name__ == "__main__":
    g = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert min_steps(g, (2, 0), (2, 2)) == 2
    assert min_steps(g, (0, 0), (2, 0)) == 2 and min_steps(g, (0, 0), (0, 0)) == 0
    assert min_steps([[0, 0, 0], [0, 0, 0]], (0, 0), (1, 0)) == 1
    assert min_steps([[0, 0, 0], [0, 0, 0]], (1, 0), (0, 0)) == 1
    # going from the top-left to the cell right below needs a South heading; coming back up needs North or three lefts
    assert min_steps([[0, 0], [0, 0]], (0, 1), (1, 1)) == 1
    rng = Random(490)
    for _ in range(300):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        grid = [[1 if rng.random() < 0.25 else 0 for _ in range(n)] for _ in range(m)]
        free = [(r, c) for r in range(m) for c in range(n) if grid[r][c] == 0]
        if len(free) < 2:
            continue
        s, t = rng.sample(free, 2)
        got, want = min_steps(grid, s, t), _brute(grid, s, t, 11)
        assert (got == want) if got != -1 and got <= 11 else (want == -1 or want == got), (grid, s, t, got, want)
    print("OK amz_directional_grid")
