---
id: lct-learn-graph-1-2
node: graph.1.2
type: qa
step: 1
---
## Q
**图论算法 › 图的遍历 › 广度优先搜索（BFS）**｜学习卡

套路是什么？

## A
**一句话。** 边权都是 `1` 时，用队列一层层向外扩，第一次到达某点的步数就是最短路；状态不一定是点，可以是（点，颜色）、线路等。

下图：从起点一层层外扩，第一次到达时的层数就是最短步数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="40" y="150" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dis 0</text>
<line x1="40" y1="10" x2="40" y2="138" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="120" y="150" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 1</text>
<line x1="120" y1="10" x2="120" y2="138" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="200" y="150" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 2</text>
<line x1="200" y1="10" x2="200" y2="138" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="280" y="150" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dis 3</text>
<line x1="280" y1="10" x2="280" y2="138" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="51.6" y1="69.2" x2="108.4" y2="40.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="51.6" y1="80.8" x2="108.4" y2="109.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="133.0" y1="35.0" x2="187.0" y2="35.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="133.0" y1="115.0" x2="187.0" y2="115.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="120.0" y1="48.0" x2="120.0" y2="102.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="211.6" y1="40.8" x2="268.4" y2="69.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="211.6" y1="109.2" x2="268.4" y2="80.8" stroke-width="1.2" stroke="currentColor"/>
<circle cx="40" cy="75" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<circle cx="120" cy="35" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120" y="39" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="120" cy="115" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="120" y="119" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="200" cy="35" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="39" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="200" cy="115" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="119" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="280" cy="75" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
</svg>

```python
def bfs(n, edges, start):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)           # 有向图只加一行
    dis = [-1] * n               # -1 表示还没到过
    dis[start] = 0
    q = deque([start])
    while q:
        x = q.popleft()
        for y in g[x]:
            if dis[y] < 0:       # 第一次到达就是最短
                dis[y] = dis[x] + 1
                q.append(y)
    return dis
```

**要点。**
- 为什么对？：队列里的距离单调不减，先出队的层更近，所以第一次入队时的距离就是最短距离；每个状态最多入队一次，`O(n + m)`。
- LC 1129 怎么改？：状态是 `(点, 最后一条边的颜色)`，只能走与上一条颜色不同的边，答案取到该点两种颜色状态的较小值。
- LC 815 怎么改？：以线路为点而不是站点：`站 → 经过它的线路列表`，上一条线路就是换乘一次，已用过的线路清空，防止重复扩展。

**易错点。**
- 入队时才标记已访问：出队时才标记会让同一点多次入队，复杂度爆炸。
- 起点就是终点：`source == target` 应返回 `0`，不能进循环后返回 `-1`。
- 状态漏掉维度：1129 只记点会把交替颜色的路径错判为不可达。

**对应题目。** LC 815 公交路线、LC 1129 颜色交替的最短路径
