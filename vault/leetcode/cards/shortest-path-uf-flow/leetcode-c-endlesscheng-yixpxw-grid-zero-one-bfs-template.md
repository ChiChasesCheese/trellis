---
id: leetcode-c-endlesscheng-yixpxw-grid-zero-one-bfs-template
node: shortest-path-uf-flow.grid-zero-one-bfs
type: cloze
anki: 1787272404907
tags: [concept-cloze, leetcode, recall, template]
---
0-1 BFS 的更新条件是 {{c1::candidate < distance[nr][nc]}}；只有成立时才更新距离并加入双端队列。

```
def min_zero_one_cost(grid, start_row, start_col, cost):
    from collections import deque

    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    inf = float('inf')
    distance = [[inf] * cols for _ in range(rows)]
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    distance[start_row][start_col] = 0
    dequeues = deque([(start_row, start_col)])

    while dequeues:
        row, col = dequeues.popleft()
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            weight = cost(row, col, nr, nc)
            if weight not in (0, 1):
                raise ValueError('edge weight must be 0 or 1')
            candidate = distance[row][col] + weight
            if candidate < distance[nr][nc]:
                distance[nr][nc] = candidate
                if weight == 0:
                    dequeues.appendleft((nr, nc))
                else:
                    dequeues.append((nr, nc))

    return distance
```

**Evidence**

三、网格图 0-1 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.03%20-%20%E7%BD%91%E6%A0%BC%200-1%20BFS)
