---
id: leetcode-c-endlesscheng-yixpxw-grid-unweighted-bfs-template
node: graphs-traversal.grid-unweighted-bfs
type: cloze
anki: 1787272404605
tags: [concept-cloze, leetcode, recall, template]
---
网格 BFS 发现未访问邻居时，应先执行 {{c1::distance[nr][nc] = distance[row][col] + 1}}，再入队。

```
def shortest_distances(grid, start_row, start_col):
    from collections import deque

    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    distance = [[-1] * cols for _ in range(rows)]
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    if grid[start_row][start_col] != '.':
        return distance

    distance[start_row][start_col] = 0
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == '.' and distance[nr][nc] == -1):
                distance[nr][nc] = distance[row][col] + 1
                queue.append((nr, nc))

    return distance
```

**Evidence**

二、网格图 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.02%20-%20%E7%BD%91%E6%A0%BC%E6%97%A0%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%20BFS)
