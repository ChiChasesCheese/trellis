"""LC 200 Number of Islands -- flood fill (BFS) from every unvisited land cell. Time O(R*C), space O(R*C)."""
from collections import deque

# --- solution ---
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != "1" or (r0, c0) in seen:
                continue
            islands += 1                                   # new island found: sink all of it
            seen.add((r0, c0))
            queue = deque([(r0, c0)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in seen:
                        seen.add((nr, nc))                 # mark when ENQUEUED, not when popped
                        queue.append((nr, nc))
    return islands
# --- end ---

if __name__ == "__main__":
    g = ["11110", "11010", "11000", "00000"]
    assert num_islands([list(r) for r in g]) == 1
    g = ["11000", "11000", "00100", "00011"]
    assert num_islands([list(r) for r in g]) == 3
    assert num_islands([]) == 0
    assert num_islands([["0"]]) == 0
    assert num_islands([["1"]]) == 1
    assert num_islands([list("101"), list("010"), list("101")]) == 5     # diagonals do not connect
    print("ok 200_number_of_islands")
