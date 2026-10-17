"""LC 490 The Maze -- BFS over STOPPING cells: from a stop, roll in each of 4 directions until the next cell is a wall."""
from collections import deque
from random import Random

# --- solution ---
def has_path(maze, start, destination):
    m, n = len(maze), len(maze[0])
    seen = {tuple(start)}
    queue = deque([tuple(start)])
    while queue:
        r, c = queue.popleft()
        if [r, c] == list(destination):                  # must STOP here, not just pass through
            return True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr, nc = nr + dr, nc + dc                # keep rolling until the next cell is wall / border
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc))
    return False
# --- end ---

def _brute(maze, start, destination):
    # state (r, c, dir): the ball is rolling in dir; it may only choose a new direction when blocked
    m, n = len(maze), len(maze[0])
    D = ((1, 0), (-1, 0), (0, 1), (0, -1))
    seen, stack = set(), [(start[0], start[1], d) for d in range(4)]
    while stack:
        r, c, d = stack.pop()
        if (r, c, d) in seen:
            continue
        seen.add((r, c, d))
        nr, nc = r + D[d][0], c + D[d][1]
        if 0 <= nr < m and 0 <= nc < n and maze[nr][nc] == 0:
            stack.append((nr, nc, d))
        else:
            if [r, c] == list(destination):
                return True
            stack.extend((r, c, e) for e in range(4) if e != d)
    return False

if __name__ == "__main__":
    maze = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]]
    assert has_path(maze, [0, 4], [4, 4]) is True
    assert has_path(maze, [0, 4], [3, 2]) is False
    assert has_path([[0, 0]], [0, 0], [0, 1]) is True
    rng = Random(490)
    for _ in range(500):
        m, n = rng.randint(1, 6), rng.randint(2, 6)
        g = [[1 if rng.random() < 0.3 else 0 for _ in range(n)] for _ in range(m)]
        free = [(r, c) for r in range(m) for c in range(n) if g[r][c] == 0]
        if len(free) < 2:
            continue
        s, t = rng.sample(free, 2)
        assert has_path(g, list(s), list(t)) == _brute(g, s, t), (g, s, t)
    print("ok 490_the_maze")
