---
id: lct-learn-graph-3-1
node: graph.3.1
type: qa
step: 1
---
## Q
**图论算法 › 最短路 › 单源最短路：Dijkstra 算法**｜学习卡

套路是什么？

## A
**一句话。** 非负边权下，用小根堆每次取出当前最近的未定点，用它松弛邻居；堆里同一点可能有多份，出堆时发现过期就跳过（懒删除）。

下图：每次从堆里取出当前最近的点，它的距离就定了，再用它松弛邻居。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<line x1="51.6" y1="69.2" x2="118.4" y2="35.8" stroke-width="1.2" stroke="currentColor"/>
<text x="91.0" y="48.5" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<line x1="51.6" y1="80.8" x2="118.4" y2="114.2" stroke-width="1.2" stroke="currentColor"/>
<text x="91.0" y="93.5" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="130.0" y1="43.0" x2="130.0" y2="107.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="136.0" y="71.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="141.9" y1="35.3" x2="218.1" y2="69.7" stroke-width="1.2" stroke="currentColor"/>
<text x="186.0" y="48.5" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<line x1="141.9" y1="114.7" x2="218.1" y2="80.3" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="186.0" y="93.5" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="240.9" y1="82.0" x2="289.1" y2="113.0" stroke-width="1.2" stroke="currentColor"/>
<text x="271.0" y="93.5" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<circle cx="40" cy="75" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="40" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">s</text>
<circle cx="130" cy="30" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="130" cy="120" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<circle cx="230" cy="75" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c</text>
<circle cx="300" cy="120" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">d</text>
<text x="40" y="103" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 0</text>
<text x="130" y="12" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 2</text>
<text x="130" y="148" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dis 3</text>
<text x="230" y="103" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 5</text>
<text x="300" y="148" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis ∞</text>
<text x="250" y="22" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实心 = 已出堆定下</text>
<text x="170" y="174" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">弹出最近的 b(3)，松弛 c：8 → 5；堆里旧的 (8, c) 出堆时跳过</text>
</svg>

```python
def dijkstra(n, edges, start):
    g = [[] for _ in range(n)]
    for x, y, w in edges:
        g[x].append((y, w))          # 无向图再加反向边
    dis = [inf] * n
    dis[start] = 0
    h = [(0, start)]                 # (起点到 x 的距离, x)
    while h:
        d, x = heappop(h)
        if d > dis[x]:               # 过期的旧记录
            continue
        for y, w in g[x]:
            nd = d + w
            if nd < dis[y]:
                dis[y] = nd
                heappush(h, (nd, y))
    return dis
```

**要点。**
- 为什么对？：边权非负，堆顶的距离不可能再被别的路径缩短，所以出堆即定；每条边最多入堆一次，`O((n + m) log m)`。
- LC 743 怎么改？：就是模板，答案是 `max(dis)`，有 `inf` 则返回 `-1`。
- LC 778 怎么改？：堆的键不用求和，改成路径上的最大高度 `max(d, 邻格高度)`，到右下角时的键就是答案（瓶颈路）。
- LC 787 怎么改？：状态多一维已坐航班数，`(价格, 点, 次数)` 入堆，次数超过 `k + 1` 不再扩展；或者做 `k + 1` 轮 Bellman-Ford。

**易错点。**
- 有负权边：「出堆即定」不再成立，结果可能错或极慢，应改用 Bellman-Ford（787 的分轮写法）。
- 忘了过期判断：不跳过会重复松弛，最坏退化成 `O(m^2)`。
- 787 只按价格去重：便宜但中转多的路径会挡住贵一点但次数少的路径，必须带次数。

**对应题目。** LC 787 K 站中转内最便宜的航班、LC 743 网络延迟时间、LC 778 水位上升的泳池中游泳
