---
id: lct-learn-list-tree-backtracking-3-1
node: list-tree-backtracking.3.1
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 一般树 › 遍历**｜学习卡

套路是什么？

## A
**一句话。** 一般树用邻接表存，DFS 多带一个父节点参数 `fa`，只要不走回头路就不会重复访问，不需要 `visited`；边上的方向、权值直接塞进邻接表。

下图：LC 1466，邻接表里存双向边并带上「是否背离 0」；DFS 只要不走回父亲就不会重复。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<line x1="99.7" y1="39.5" x2="60.3" y2="75.5" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.3,75.5 63.0,69.0 67.0,73.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="50.0" y1="99.0" x2="50.0" y2="131.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50.0,131.0 47.0,124.7 53.0,124.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="96.0" y1="145.0" x2="64.0" y2="145.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="64.0,145.0 70.3,142.0 70.3,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="159.7" y1="75.5" x2="120.3" y2="39.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.3,39.5 127.0,41.6 123.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170.0" y1="99.0" x2="170.0" y2="131.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,131.0 167.0,124.7 173.0,124.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<circle cx="110" cy="30" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="50" cy="85" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="170" cy="85" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="50" cy="145" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="170" cy="145" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="110" cy="145" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="110" y="12" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从 0 出发</text>
<text x="215" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">蓝色边背离 0：要翻转</text>
<text x="215" y="58" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">黑色边朝向 0：不用翻</text>
<text x="215" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">dfs(x, fa)：</text>
<text x="215" y="106" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">跳过 y == fa</text>
<text x="215" y="122" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不需要 visited</text>
<text x="215" y="150" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">答案 = 3</text>
</svg>

```python
def min_reorder(n, connections):     # LC 1466
    g = [[] for _ in range(n)]
    for a, b in connections:         # 原来的边 a -> b
        g[a].append((b, 1))          # 从 a 走向 b：背离 0，需翻转
        g[b].append((a, 0))          # 从 b 走向 a：朝向 0，不用翻
    def dfs(x, fa):
        cnt = 0
        for y, need in g[x]:
            if y != fa:              # 不走回头路，树里不需要 visited
                cnt += need + dfs(y, x)
        return cnt
    return dfs(0, -1)
```

**要点。**
- 为什么只排除父亲就够？：树里任意两点只有一条路径，到达 `x` 时若某个邻居 `y != fa` 已访问过，`x` 与 `y` 之间就有两条路径，与无环矛盾；每个点恰访问一次，`O(n)`。
- LC 1466 为什么数背离根的边？：所有城市都要走到 `0`，等价于每条树边都朝向根；原方向是「父 → 子」的边必须翻转，各条边互不影响。
- LC 2368 怎么改？：受限点放进集合，遇到既不计数也不递归，`dfs` 返回连通块大小；给 `parent` 数组的题（LC 582）先建「父 → 孩子」的有向表，就不需要 `fa`。

**易错点。**
- 忘了排除父亲：`edges = [[0, 1]]` 会 `0 -> 1 -> 0 -> …` 无限递归。
- 方向标记写反：`n = 3`、`connections = [[1,0],[2,0]]` 已都指向 `0`，应得 `0`。
- 链状树 `n = 10^5` 递归栈溢出：改 BFS 或迭代 DFS，仍靠 `fa` 防回头。

**对应题目。** LC 1466 重新规划路线
