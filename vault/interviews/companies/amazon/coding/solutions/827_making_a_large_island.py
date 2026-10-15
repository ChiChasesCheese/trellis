"""LC 827 Making A Large Island -- union-find with component sizes; try flipping each 0 by summing distinct neighbours."""
from random import Random

# --- solution ---
def largest_island(grid):
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    size = [1] * (rows * cols)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]:
                for dr, dc in ((1, 0), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if nr < rows and nc < cols and grid[nr][nc]:
                        union(r * cols + c, nr * cols + nc)
    best = max((size[find(i)] for i in range(rows * cols) if grid[i // cols][i % cols]), default=0)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                roots = set()                                    # a SET: one island touching the cell twice counts once
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                        roots.add(find(nr * cols + nc))
                best = max(best, 1 + sum(size[x] for x in roots))
    return best
# --- end ---

def _biggest(grid):
    rows, cols, seen, best = len(grid), len(grid[0]), set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] and (r, c) not in seen:
                stack, n = [(r, c)], 0
                seen.add((r, c))
                while stack:
                    a, b = stack.pop()
                    n += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        x, y = a + dr, b + dc
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                best = max(best, n)
    return best

def _brute(grid):
    best = _biggest(grid)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                grid[r][c] = 1
                best = max(best, _biggest(grid))
                grid[r][c] = 0
    return best

if __name__ == "__main__":
    assert largest_island([[1, 0], [0, 1]]) == 3
    assert largest_island([[1, 1], [1, 0]]) == 4
    assert largest_island([[1, 1], [1, 1]]) == 4
    assert largest_island([[0]]) == 1
    assert largest_island([[0, 0], [0, 0]]) == 1
    assert largest_island([[1, 0, 1], [0, 0, 0], [1, 0, 1]]) == 3
    rng = Random(59)
    for _ in range(500):
        r, c = rng.randint(1, 5), rng.randint(1, 5)
        g = [[rng.randint(0, 1) for _ in range(c)] for _ in range(r)]
        assert largest_island(g) == _brute(g), g
    print("ok 827_making_a_large_island")
