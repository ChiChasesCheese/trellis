"""LC 994 Rotting Oranges -- multi-source BFS, one level per minute. Time O(R*C), space O(R*C)."""
from collections import deque

# --- solution ---
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))                  # ALL rotten oranges start together (level 0)
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):                   # process exactly one level = one minute
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1
# --- end ---

if __name__ == "__main__":
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1     # bottom-left is unreachable
    assert oranges_rotting([[0, 2]]) == 0                                # nothing fresh
    assert oranges_rotting([[0]]) == 0
    assert oranges_rotting([[1]]) == -1                                  # fresh but no rotten source
    print("ok 994_rotting_oranges")
