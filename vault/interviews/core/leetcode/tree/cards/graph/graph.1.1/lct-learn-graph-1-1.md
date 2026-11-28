---
id: lct-learn-graph-1-1
node: graph.1.1
type: qa
step: 1
---
## Q
**图论算法 › 图的遍历 › 深度优先搜索（DFS）**｜学习卡

套路是什么？

## A
**一句话。** 建邻接表，对每个没访问过的点启动一次 DFS，进门先标记；启动次数就是连通块个数，DFS 返回值可以带回块大小，遇到已在栈中的点（有向图）就是环。

下图：对每个没访问过的点启动一次 DFS，一次标记完整个连通块。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<line x1="52.8" y1="37.9" x2="87.2" y2="32.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="46.2" y1="51.4" x2="63.8" y2="83.6" stroke-width="1.2" stroke="currentColor"/>
<line x1="83.0" y1="95.0" x2="117.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="105.4" y1="41.8" x2="124.6" y2="83.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="231.6" y1="45.8" x2="268.4" y2="64.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="269.8" y1="78.1" x2="240.2" y2="101.9" stroke-width="1.2" stroke="currentColor"/>
<circle cx="40" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<circle cx="100" cy="30" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="100" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="70" cy="95" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="70" y="99" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="130" cy="95" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130" y="99" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="220" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="220" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<circle cx="280" cy="70" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="280" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="230" cy="110" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="230" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">6</text>
<text x="40" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 1 次启动</text>
<text x="220" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 2 次启动</text>
<text x="170" y="142" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">进门先标记；启动次数 = 块数，返回值累加 = 块大小</text>
</svg>

```python
def components(n, edges):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)           # 有向图只加一行
    vis = [False] * n

    def dfs(x):
        vis[x] = True            # 进门先标记，避免重复访问
        size = 1
        for y in g[x]:
            if not vis[y]:
                size += dfs(y)
        return size

    return [dfs(i) for i in range(n) if not vis[i]]
```

**要点。**
- 为什么对？：每个点只被标记一次，每条边只看两遍，`O(n + m)`；外层循环里每次启动 DFS，恰好覆盖一个新的连通块。
- LC 261 / 323 怎么改？：数连通块个数 `len(components(...))`；以图判树就是 `m == n - 1` 且连通块个数为 `1`。
- LC 207 怎么改？：有向图，状态用三色（`0` 未访问、`1` 在当前递归栈、`2` 已完成），遇到 `1` 说明有环。
- LC 924 / 3387 怎么改？：先找出每个块的大小或所含点，再在块上做统计；3387 是两天分别在两张汇率图上 DFS 乘汇率。

**易错点。**
- 有向图当无向图建边：`0 → 1`、`1 → 0` 才是环，只有 `0 → 1` 不是。
- 无向图判环忘记父节点：`0 - 1` 一条边，从 `1` 回看 `0` 不是环。
- 忘了外层循环：图不连通时只从 `0` 出发会漏掉其他块。

**对应题目。** LC 207 课程表、LC 261 Graph Valid Tree、LC 3387 两天自由外汇交易后的最大货币数、LC 924 尽量减少恶意软件的传播、LC 323 无向图中连通分量的数目、LC 547 省份数量
