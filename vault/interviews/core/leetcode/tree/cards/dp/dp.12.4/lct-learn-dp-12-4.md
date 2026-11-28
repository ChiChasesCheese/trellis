---
id: lct-learn-dp-12-4
node: dp.12.4
type: qa
step: 1
---
## Q
**动态规划 › 树形 DP › 换根 DP**｜学习卡

套路是什么？

## A
**一句话。** 换根 DP：先以 `0` 为根算出 `ans[0]`，再从根往下推，相邻两点的答案只差那一条边的朝向，`ans[v] = ans[u] ± 1`。

下图：LC 2858，先算出一个根的答案，再沿边往下推，相邻两点只差一条边。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<line x1="100.5" y1="40.3" x2="59.5" y2="84.7" stroke-width="1.2" stroke="currentColor"/>
<polygon points="59.5,84.7 61.6,78.0 66.0,82.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="119.5" y1="40.3" x2="160.5" y2="84.7" stroke-width="1.2" stroke="currentColor"/>
<polygon points="160.5,84.7 154.0,82.1 158.4,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170.0" y1="109.0" x2="170.0" y2="141.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,141.0 167.0,134.7 173.0,134.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="110" cy="30" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="50" cy="95" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="50" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="170" cy="95" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="99" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="170" cy="155" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="68" y="99" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans 1</text>
<text x="128" y="34" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans 0</text>
<text x="188" y="99" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans 1</text>
<text x="188" y="159" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans 2</text>
<text x="225" y="30" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">以 0 为根：ans[0] = 1</text>
<text x="225" y="56" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">根从 u 挪到 v：</text>
<text x="225" y="72" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">只有 u-v 这条边</text>
<text x="225" y="88" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">的「要不要反转」变了</text>
<text x="225" y="114" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">原边 u→v：+1</text>
<text x="225" y="130" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">原边 v→u：-1</text>
</svg>

```python
def min_edge_reversals(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append((v, 0))          # 顺着走，不用反转
        g[v].append((u, 1))          # 逆着走，要反转
    ans = [0] * n

    def count(u, p):                 # 以 0 为根要反转几条
        return sum(w + count(v, u)
                   for v, w in g[u] if v != p)

    def reroot(u, p):
        for v, w in g[u]:
            if v != p:
                ans[v] = ans[u] + (1 if w == 0 else -1)
                reroot(v, u)

    ans[0] = count(0, -1)
    reroot(0, -1)
    return ans
```

**要点。**
- 为什么对？：边 `(u,v)` 把树分成两侧，两侧内部边的朝向要求都不变，换根只影响这条边自己：原来朝外现在要反转 `+1`，原来要反转现在不用 `-1`。
- LC 834 怎么改？：`ans[v] = ans[u] - size[v] + (n - size[v])`，先一遍后序求子树大小和 `ans[0]`。

**易错点。**
- 换根时符号写反：示例一得 `[1,1,2,0]`，应为 `[1,1,0,2]`。
- 对每个节点各 DFS 一次：`O(n^2)`，`n = 10^5` 超时。
- 链状输入递归太深：`10^5` 层会 `RecursionError`，要调高递归上限或改迭代。

**对应题目。** LC 2858 可以到达每一个节点的最少边反转次数
