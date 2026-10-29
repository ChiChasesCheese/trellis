---
id: uth-gaps-bfs-1-queue-vs-stack
node: gaps.bfs
type: qa
step: 1
---
## Q
**爬虫先抓近的还是先钻深**｜Scrapy · 2.19

爬虫抓完首页，拿到 20 个链接。这些链接放进「待抓清单」，下一个取哪一个？取法不同，访问顺序差在哪？

## A
**背景。** 待抓清单有两种取法。后进先出（LIFO，栈）：先取刚发现的，顺着一条链接一路钻到底再回头，叫深度优先（DFS）。先进先出（FIFO，队列）：先取最早发现的，于是先把离首页 1 次点击的页面抓完，再抓 2 次点击的，叫广度优先（BFS）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 172">
<text x="88" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">先进先出 BFS</text>
<line x1="80.2" y1="45.1" x2="57.8" y2="70.9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="95.8" y1="45.1" x2="118.2" y2="70.9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="44.3" y1="90.5" x2="31.7" y2="113.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="55.7" y1="90.5" x2="68.3" y2="113.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="126" y1="92" x2="126" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="88" cy="36" r="12" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="88" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<circle cx="50" cy="80" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<circle cx="126" cy="80" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="126" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<circle cx="26" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="26" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<circle cx="74" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<circle cx="126" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="126" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<text x="88" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">一层一层往外</text>
<text x="252" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">后进先出 DFS</text>
<line x1="244.2" y1="45.1" x2="221.8" y2="70.9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="259.8" y1="45.1" x2="282.2" y2="70.9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="208.3" y1="90.5" x2="195.7" y2="113.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="219.7" y1="90.5" x2="232.3" y2="113.5" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="290" y1="92" x2="290" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="252" cy="36" r="12" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<circle cx="214" cy="80" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="214" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<circle cx="290" cy="80" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="290" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<circle cx="190" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="190" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<circle cx="238" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="238" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<circle cx="290" cy="124" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="290" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<text x="252" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">钻到底再回头</text>
</svg>
```

**结构。** Scrapy 默认后进先出，所以默认是 DFS，官方说这通常最方便。要改成 BFS 得设三项：

- `DEPTH_PRIORITY = 1`
- `SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"`
- `SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"`

**细节。**

- BFS 的清单要装下整整一层：每页 20 个链接，第 3 层就可能有 8000 个待抓；DFS 只留当前路径上的兄弟
- 开头几个请求是并发发出的，顺序会乱；把 `CONCURRENT_REQUESTS` 降到 1 才严格

**例题：** LC 200 岛屿数量（同类：LC 102 二叉树的层序遍历）

给 `'1'`（陆地）和 `'0'`（水）组成的二维网格，陆地只按水平或竖直方向相连成岛，求岛屿总数。例：`[["1","1","0"],["0","0","1"]]` → 2。用 `deque` 做 BFS，一次淹没一整座岛。

```python
from collections import deque

def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(sr: int, sc: int) -> None:
        queue = deque([(sr, sc)])
        grid[sr][sc] = "0"  # 入队即淹没，避免重复入队
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    queue.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```
