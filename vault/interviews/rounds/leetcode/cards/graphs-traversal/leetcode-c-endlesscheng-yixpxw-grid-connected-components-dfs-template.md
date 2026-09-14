---
id: leetcode-c-endlesscheng-yixpxw-grid-connected-components-dfs-template
node: graphs-traversal.grid-connected-components-dfs
type: cloze
anki: 1787272404304
tags: [concept-cloze, leetcode, recall, template]
---
连通块 DFS 的相邻扩展条件应同时检查 {{c1::未越界、可通行、未访问}}。

```
def component_sizes(grid):
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def dfs(row, col):
        visited[row][col] = True
        size = 1
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == '.' and not visited[nr][nc]):
                size += dfs(nr, nc)
        return size

    sizes = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '.' and not visited[row][col]:
                sizes.append(dfs(row, col))
    return sizes
```

**Evidence**

一、网格图 DFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.01%20-%20%E7%BD%91%E6%A0%BC%E8%BF%9E%E9%80%9A%E5%9D%97%20DFS)
