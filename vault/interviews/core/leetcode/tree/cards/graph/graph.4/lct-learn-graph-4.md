---
id: lct-learn-graph-4
node: graph.4
type: qa
step: 1
---
## Q
**图论算法 › 最小生成树**｜学习卡

套路是什么？

## A
**一句话。** Kruskal：边按权从小到大排序，用并查集逐条加边，两端已连通就跳过；选够 `n - 1` 条边就是最小生成树。稠密图（如完全图）用 Prim：每轮把离已选集合最近的点并进来。

下图：Kruskal 从最轻的边起逐条加，成环的边跳过。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<line x1="63.0" y1="40.0" x2="157.0" y2="40.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="116.0" y="36.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="50.0" y1="53.0" x2="50.0" y2="107.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="56.0" y="76.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="170.0" y1="53.0" x2="170.0" y2="107.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="176.0" y="76.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<line x1="63.0" y1="120.0" x2="157.0" y2="120.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="116.0" y="116.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="60.8" y1="47.2" x2="159.2" y2="112.8" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="116.0" y="76.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<circle cx="50" cy="40" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="170" cy="40" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="50" cy="120" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="170" cy="120" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<text x="210" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">边按权升序：1 2 3 选</text>
<text x="210" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4、5 两端已连通：跳过</text>
<text x="210" y="86" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">并查集判连通</text>
<text x="210" y="104" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">选够 n - 1 条即止</text>
</svg>

```python
def kruskal(n, edges):
    fa = list(range(n))

    def find(x):                     # 路径压缩
        if fa[x] != x:
            fa[x] = find(fa[x])
        return fa[x]

    total = cnt = 0
    for x, y, w in sorted(edges, key=lambda e: e[2]):
        rx, ry = find(x), find(y)
        if rx != ry:                 # 不连通才选这条边
            fa[rx] = ry
            total += w
            cnt += 1
    return total if cnt == n - 1 else inf   # 不连通
```

**要点。**
- 为什么对？：割性质：连接任意两部分的最小边必在某棵最小生成树里；按权升序时，当前边若连通了两个不同的块，它就是这个割上的最小边。
- LC 1584 怎么改？：完全图有 `n^2` 条边，用 Prim：`d[i]` 是点 `i` 到已选集合的最近距离，每轮选最小的并更新，`O(n^2)`；Kruskal 要排序 `n^2` 条边，稍慢。
- 最大生成树怎么改？：边权从大到小排序，其余不变。

**易错点。**
- 忘了判连通：边数选不够 `n - 1` 说明图不连通，不能直接返回权和。
- Prim 误写成累加路径：那是 Dijkstra，生成树只比较单条边权，`d[j] = min(d[j], 边(新点, j))`。

**对应题目。** LC 1584 连接所有点的最小费用
