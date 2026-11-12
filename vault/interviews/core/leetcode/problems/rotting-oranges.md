---
slug: rotting-oranges
---
## Q
**LC 994 腐烂的橘子**｜Medium

网格里 `2` 是烂橘子，`1` 是新鲜橘子；每分钟烂橘子把上下左右的新鲜橘子变烂。求全部变烂的最少分钟数，做不到返回 `-1`。

## A
**一句话。** 所有烂橘子同时入队做多源 BFS，一层就是一分钟。

```python
def oranges_rotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque((i, j) for i in range(m) for j in range(n)
              if grid[i][j] == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while q and fresh:          # 没有新鲜的就停，不多算一分钟
        minutes += 1
        for _ in range(len(q)):  # 处理完一层 = 一分钟
            i, j = q.popleft()
            for x, y in ((i+1, j), (i-1, j),
                         (i, j+1), (i, j-1)):
                if (0 <= x < m and 0 <= y < n
                        and grid[x][y] == 1):
                    grid[x][y] = 2       # 入队即标记
                    fresh -= 1
                    q.append((x, y))
    return -1 if fresh else minutes
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 循环只写 `while q`：最后一层之后还会多数一分钟，`[[0,2]]` 得 `1`，应为 `0`。
- 忘了最后检查 `fresh`：有永远烂不到的橘子要返回 `-1`。

**追问。**
- 不许改输入网格？：另开 `time[i][j]` 记腐烂时刻，兼作 visited。
- 为什么不用 DFS？：DFS 先到的不一定最早，要反复更新；BFS 按层走，先到即最早。

**同模式。** LC 542 01 矩阵、LC 286 墙与门、LC 1162 地图分析
