---
id: uth-gaps-bfs-2-depth-buckets
node: gaps.bfs
type: qa
step: 2
---
## Q
**Scrapy 怎样让近的先抓**｜Scrapy · 2.19 调度器

调度器只有「优先级」这一个排序旋钮，`DEPTH_PRIORITY = 1` 怎样把它变成一层一层地抓？

## A
**结构。** 调度器里是一个字典：每个优先级一个先进先出的桶，永远先从优先级最高的非空桶里取。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 178">
<text x="14" y="45" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">深度 0</text>
<rect x="82" y="30" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="14" y="87" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">深度 1</text>
<rect x="82" y="72" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="114" y="72" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="146" y="72" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="14" y="129" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">深度 2</text>
<rect x="82" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="114" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="146" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="178" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="210" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="242" y="114" width="26" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82" y="22" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每个深度一个先进先出的桶</text>
<line x1="310" y1="30" x2="310" y2="130" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M310,136 L306.5,129 L313.5,129 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="310" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">先取</text>
<text x="310" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">后取</text>
<text x="14" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">优先级 = 负的深度 浅的桶先出</text>
</svg>
```

**细节。**

- 深度中间件给每个新请求 `priority -= depth * DEPTH_PRIORITY`：深度 1 的优先级 -1，深度 2 的 -2
- 内部键 = 负的优先级 = 深度，取最小的键：浅的桶先出，桶内先进先出
- `DEPTH_PRIORITY` 设为负数，就是深度优先
- 默认调度器还按域名分开，每个域名各有一套桶

**为什么。** 层号直接当优先级存着，不用像手写 BFS 那样每轮数一遍队列长度来划层。

**例题：** LC 994 腐烂的橘子（同类：LC 1091 二进制矩阵中的最短路径）

`m x n` 网格：`0` 空、`1` 新鲜橘子、`2` 腐烂橘子。每分钟，腐烂橘子上下左右的新鲜橘子都会腐烂。求所有橘子腐烂所需的最少分钟数，做不到返回 -1。例：`[[2,1,1],[1,1,0],[0,1,1]]` → 4。一层就是一分钟。

```python
from collections import deque


def oranges_rotting(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    queue = deque((i, j) for i, row in enumerate(grid) for j, v in enumerate(row) if v == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while queue and fresh:                     # 没有新鲜橘子就立刻停，不多算一分钟
        minutes += 1
        for _ in range(len(queue)):            # 恰好处理完当前这一层 = 过去一分钟
            i, j = queue.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2           # 入队时就标记，避免重复入队
                    fresh -= 1
                    queue.append((ni, nj))
    return -1 if fresh else minutes
```
