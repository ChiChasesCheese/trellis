---
id: uth-gaps-shortest-path-1-spf
node: gaps.shortest-path
type: qa
step: 1
---
## Q
**路由器怎样算出每个目的地走哪**｜OSPF · FRRouting 10.7

路由器收到一个发往某网段的包，怎么知道该交给哪个邻居？几十台路由器的网络，谁来算这张表？

## A
**背景。** 最朴素的办法：每台路由器只和邻居交换「我到各网段有多远」，一站站传下去（RIP）。各台只听说、没见过全貌，出故障时错误的距离会来回传、一点点涨，涨到「无穷」才停（RIP 把 16 当无穷）。OSPF 的办法：每台路由器把「我和谁相连、代价多少」洪泛（flooding，逐跳转发给所有路由器），人人手里有同一张完整的地图，各自以自己为起点算最短路。

**结构。** Dijkstra：起点先进树；每次从候选（已发现、最短路还没定的路由器）里取离起点最近的一台进树，再看它的邻居能否给出更短的路；取空为止。结果是以自己为根的最短路径树，到某网段的下一跳（next hop）就是树上从根出发的第一步。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<line x1="52.5" y1="91.7" x2="117.5" y2="48.3" fill="none" stroke="currentColor" stroke-width="2.6" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="52.5" y1="108.3" x2="117.5" y2="151.7" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="130" y1="55" x2="130" y2="145" fill="none" stroke="currentColor" stroke-width="2.6" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="143.2" y1="47.2" x2="226.8" y2="92.8" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="143.2" y1="152.8" x2="226.8" y2="107.2" fill="none" stroke="currentColor" stroke-width="2.6" style="stroke:var(--accent,#3b6fd4)"/>
<text x="72" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="66" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4</text>
<text x="146" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="200" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">5</text>
<text x="200" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">1</text>
<circle cx="40" cy="100" r="14" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="40" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<circle cx="130" cy="40" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<circle cx="130" cy="160" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<circle cx="240" cy="100" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="240" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">D</text>
<text x="40" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">距离 0</text>
<text x="130" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">距离 1</text>
<text x="130" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">距离 3</text>
<text x="240" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">距离 4</text>
<text x="170" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">粗线 = 最短路径树 A 去 D 先走 B</text>
</svg>
```

例：A 到 C，直连代价 4，经 B 是 1 + 2 = 3，更短，所以 C 的下一跳是 B。

**例题：** LC 778 水位上升的泳池中游泳（同类：LC 787 K 站中转内最便宜的航班）

`n x n` 矩阵 `grid`，`grid[i][j]` 是平台高度，时间 `t` 时水位为 `t`；水位不低于相邻两个平台的高度时才能游过去。从左上角走到右下角，求最少时间。例：`[[0,2],[1,3]]` → 3。这是 Dijkstra 的变体：路径长度不是边权之和，而是路径上的最大高度，所以把 `+` 换成 `max`。

```python
from heapq import heappop, heappush


def swim_in_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]                    # (到达此格所需的最低水位, 行, 列)
    seen = {(0, 0)}
    while heap:
        t, x, y = heappop(heap)                    # 弹出的是"当前最低水位下能到的最低一格"
        if x == y == n - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in seen:
                seen.add((nx, ny))
                heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return -1
```
