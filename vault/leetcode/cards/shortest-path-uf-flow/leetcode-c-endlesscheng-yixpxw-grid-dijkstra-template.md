---
id: leetcode-c-endlesscheng-yixpxw-grid-dijkstra-template
node: shortest-path-uf-flow.grid-dijkstra
type: cloze
anki: 1787272405205
tags: [concept-cloze, leetcode, recall, template]
---
Dijkstra 的松弛步骤是：若 {{c1::current + weight < distance[nr][nc]}}，更新距离并将新三元组压入最小堆。

```
def min_costs(grid, start_row, start_col, cost):
    import heapq

    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    inf = float('inf')
    distance = [[inf] * cols for _ in range(rows)]
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    distance[start_row][start_col] = 0
    heap = [(0, start_row, start_col)]

    while heap:
        current, row, col = heapq.heappop(heap)
        if current != distance[row][col]:
            continue
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            weight = cost(row, col, nr, nc)
            if weight < 0:
                raise ValueError('edge weight must be nonnegative')
            candidate = current + weight
            if candidate < distance[nr][nc]:
                distance[nr][nc] = candidate
                heapq.heappush(heap, (candidate, nr, nc))

    return distance
```

**Evidence**

四、网格图 Dijkstra

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.04%20-%20%E7%BD%91%E6%A0%BC%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF)
