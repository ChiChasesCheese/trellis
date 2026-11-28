---
id: lct-learn-graph-2-1
node: graph.2.1
type: qa
step: 1
---
## Q
**图论算法 › 拓扑排序 › 拓扑排序**｜学习卡

套路是什么？

## A
**一句话。** 统计每个点的入度，入度为 `0`（没有未满足的前置）的点入队；出队时把它指向的点入度减一，减到 `0` 就入队；出队总数小于 `n` 说明有环（LC 210 就是模板本身）。

下图：入度就是还没满足的前置数；入度为 0 的点可以先做。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<line x1="51.9" y1="64.7" x2="118.1" y2="35.3" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.1,35.3 113.5,40.6 111.1,35.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="51.9" y1="75.3" x2="118.1" y2="104.7" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.1,104.7 111.1,104.9 113.5,99.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="141.9" y1="35.3" x2="208.1" y2="64.7" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.1,64.7 201.1,64.9 203.5,59.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="141.9" y1="104.7" x2="208.1" y2="75.3" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.1,75.3 203.5,80.6 201.1,75.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="40" cy="70" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<circle cx="130" cy="30" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="130" cy="110" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="220" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<text x="40" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">入度 0</text>
<text x="130" y="12" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入度 1</text>
<text x="130" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入度 1</text>
<text x="220" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入度 2</text>
<text x="252" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">入度 0 入队</text>
<text x="252" y="116" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">出队：后继 -1</text>
<text x="252" y="132" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">减到 0 入队</text>
<text x="20" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">出队顺序 0 1 2 3；出队数 &lt; n 有环</text>
</svg>

```python
def topo_sort(n, edges):
    g = [[] for _ in range(n)]
    in_deg = [0] * n
    for x, y in edges:               # x 必须排在 y 前面
        g[x].append(y)
        in_deg[y] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        x = q.popleft()
        order.append(x)
        for y in g[x]:
            in_deg[y] -= 1           # x 已完成，y 少一个前置
            if in_deg[y] == 0:
                q.append(y)
    return order if len(order) == n else []   # 有环返回空
```

**要点。**
- 为什么对？：出队的点前置全部已完成，所以边总是从前往后指；环上的点入度永远减不到 `0`，进不了队，因此 `len(order) < n` 等价于有环。
- LC 269 怎么改？：相邻两词的第一个不同字母 `a, b` 连边 `a → b`，点是出现过的字母；后词是前词的真前缀时直接判无解。
- LC 2115 怎么改？：点是菜和原材料，入度是菜缺的原材料数，初始队列是已有原材料；出队的菜加入答案。
- LC 310 怎么改？：无向图反复剥度为 `1` 的叶子，剩 `1` 或 `2` 个点就是根。

**易错点。**
- 边方向反了：先修课 `[a, b]` 表示 `b → a`，连成 `a → b` 会得到相反的顺序。
- 269 忘了孤立字母：没有边的字母也要出现在结果里，入度表要覆盖所有字母。
- 310 `n = 1`：没有叶子可剥，直接返回 `[0]`。

**对应题目。** LC 269 火星词典、LC 210 课程表 II、LC 2115 从给定原材料中找到所有可以做出的菜、LC 310 最小高度树
