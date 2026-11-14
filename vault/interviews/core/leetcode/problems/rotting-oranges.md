---
slug: rotting-oranges
---
## Q
**LC 994 腐烂的橘子**｜Medium

网格里 `2` 是烂橘子，`1` 是新鲜橘子；每分钟烂橘子把上下左右的新鲜橘子变烂。求全部变烂的最少分钟数，做不到返回 `-1`。

## A
**一句话。** 所有烂橘子同时入队做多源 BFS，一层就是一分钟。

**图解。** 格中数字是第几分钟烂掉，同一层 BFS 同一分钟，最后一层是答案。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 130">
<rect x="24" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.5" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="58" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.38" stroke="currentColor" stroke-width="1.2"/>
<text x="75.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.27" stroke="currentColor" stroke-width="1.2"/>
<text x="109.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="24" y="48" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.38" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="58" y="48" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.27" stroke="currentColor" stroke-width="1.2"/>
<text x="75.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="92" y="48" width="34" height="34" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="24" y="82" width="34" height="34" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="58" y="82" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.17" stroke="currentColor" stroke-width="1.2"/>
<text x="75.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="92" y="82" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.09" stroke="currentColor" stroke-width="1.2"/>
<text x="109.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="150" y="32" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">格中数字：第几分钟烂掉</text>
<text x="150" y="54" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0 是一开始就烂的</text>
<text x="150" y="76" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">灰格是空地</text>
<text x="150" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最后一层 = 4 分钟</text>
</svg>

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
