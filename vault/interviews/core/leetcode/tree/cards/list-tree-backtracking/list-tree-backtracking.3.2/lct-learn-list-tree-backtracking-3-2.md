---
id: lct-learn-list-tree-backtracking-3-2
node: list-tree-backtracking.3.2
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 一般树 › 自顶向下 DFS**｜学习卡

套路是什么？

## A
**一句话。** 一般树自顶向下 DFS：从根出发，把「根到当前点的累积信息」随递归一路传给孩子，用 `parent` 参数避免走回头路；任意两点之间的量由它们各自的累积值组合出来。

下图：根到每个点的累积乘数一路往下传；任意两点之比由两个累积值相除得到。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<line x1="72.8" y1="35.8" x2="47.2" y2="74.2" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="87.2" y1="35.8" x2="112.8" y2="74.2" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="40.0" y1="98.0" x2="40.0" y2="132.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="80" cy="25" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="40" cy="85" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="120" cy="85" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<circle cx="40" cy="145" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="42" y="52" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×2</text>
<text x="116" y="52" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×3</text>
<text x="26" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×4</text>
<text x="100" y="29" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ratio 1</text>
<text x="60" y="89" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="140" y="89" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="60" y="149" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="185" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ratio[v] = ratio[u] × 边乘数</text>
<text x="185" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从根一路往下传</text>
<text x="185" y="96" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">查询 (2, 3)：</text>
<text x="185" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ratio[3] / ratio[2] = 8 / 3</text>
<text x="185" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">取模时除法 = 乘逆元</text>
</svg>

```python
MOD = 10**9 + 7

def unit_conversion(conversions, queries):
    n = len(conversions) + 1
    g = [[] for _ in range(n)]       # (邻居, 乘数, 乘数的逆元)
    for s, t, f in conversions:
        inv = pow(f, -1, MOD)
        g[s].append((t, f, inv))
        g[t].append((s, inv, f))     # 反向边取逆元
    ratio = [1] * n                  # 根换成 v 的倍数
    inv_ratio = [1] * n
    def dfs(u, parent):
        for v, mul, inv in g[u]:
            if v != parent:          # 树无环，只需排除父亲
                ratio[v] = ratio[u] * mul % MOD
                inv_ratio[v] = inv_ratio[u] * inv % MOD
                dfs(v, u)
    dfs(0, -1)
    return [ratio[b] * inv_ratio[a] % MOD
            for a, b in queries]
```

**要点。**
- 为什么对？：树上任意 `a → b` 的换算都可以绕道根：先从 `a` 回到根（乘 `inv_ratio[a]`），再从根到 `b`（乘 `ratio[b]`），中间公共路径恰好抵消。
- 除法怎么处理？：结果是分数，只能在模意义下乘逆元 `pow(f, -1, MOD)`，不能整除。
- 深度很大怎么改？：链状树递归会超过 CPython 的递归上限，改成 BFS，出队时更新未访问的邻居，逻辑不变。

**易错点。**
- 反向边忘了取逆元：`1` 个 `t` 是 `1/f` 个 `s`，`s → t` 乘 `f`，`t → s` 要乘 `inv`。
- 用 `//` 做除法：分数被截断，`1 / 2` 应对应 `500000004`。
- 没传 `parent`：无向邻接表会回到父亲，无限递归。

**对应题目。** LC 3535 单位转换 II
