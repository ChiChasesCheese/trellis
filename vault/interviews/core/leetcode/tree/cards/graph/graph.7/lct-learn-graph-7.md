---
id: lct-learn-graph-7
node: graph.7
type: qa
step: 1
---
## Q
**图论算法 › 二分图染色**｜学习卡

套路是什么？

## A
**一句话。** 二分图等价于无奇环：对每个连通块任选起点染色，邻居必须染相反色，遇到与自己同色的邻居就不是二分图。

下图：邻居必须染相反色；能染完就是二分图，出现同色邻居就有奇环。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<line x1="53.0" y1="40.0" x2="97.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="110.0" y1="53.0" x2="110.0" y2="97.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="97.0" y1="110.0" x2="53.0" y2="110.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="40.0" y1="97.0" x2="40.0" y2="53.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="40" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<circle cx="110" cy="40" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="110" cy="110" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<circle cx="40" cy="110" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="40" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<text x="75" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">偶环：两色交替 ✓</text>
<line x1="233.0" y1="40.0" x2="277.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="283.8" y1="51.4" x2="261.2" y2="93.6" stroke-width="1.2" stroke="currentColor"/>
<line x1="248.8" y1="93.6" x2="226.2" y2="51.4" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="220" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<circle cx="290" cy="40" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="290" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="255" cy="105" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255" y="109" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="255" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">奇环：0、2 同色冲突 ✗</text>
</svg>

```python
def is_bipartite(n, edges):
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)
    color = [0] * n                  # 0 未染色，1 和 2 两种颜色

    def dfs(x, c):
        color[x] = c
        for y in g[x]:
            if color[y] == c:        # 邻居同色：奇环
                return False
            if color[y] == 0 and not dfs(y, 3 - c):
                return False
        return True

    # 图可能有多个连通块，每块都要染一次
    return all(color[i] or dfs(i, 1) for i in range(n))
```

**要点。**
- 为什么对？：二分图的每条边两端异色，沿着任何路径颜色必须交替，所以奇环必然冲突、偶环不会；DFS 与 BFS 染色都可以。
- LC 785 怎么改？：就是模板，输入已是邻接表，不用建图。
- LC 886 怎么改？：每对「互相讨厌」连一条无向边，能染成两色就能分成两组。

**易错点。**
- 只从点 `0` 出发：`[[1],[0],[3],[2]]` 有两个连通块，其他块的奇环会漏判。
- 用 `visited` 代替颜色：只知道访问过，不知道要和谁异色。
- 886 编号从 `1` 开始：开 `n + 1` 个位置，或统一减一。

**对应题目。** LC 785 判断二分图、LC 886 可能的二分法
