---
slug: unit-conversion-ii
---
## Q
**LC 3535 单位转换 II**｜Medium

`n` 个单位构成一棵转换树，`1` 个 `source` 等于 `factor` 个 `target`。每次查询求 `1` 个 `A` 等于多少个 `B`，答案对 `10^9+7` 取模（分数用逆元）。

## A
**一句话。** 从单位 `0` 做 DFS 算出 `ratio[v]` 及其逆元，查询答案是 `ratio[B] * inv_ratio[A]`。

```python
MOD = 10**9 + 7

def unit_conversion(conversions, queries):
    n = len(conversions) + 1
    g = [[] for _ in range(n)]    # (邻居, 乘数, 乘数的逆元)
    for s, t, f in conversions:
        inv = pow(f, -1, MOD)
        g[s].append((t, f, inv))
        g[t].append((s, inv, f))  # 反向取逆元
    ratio = [1] * n               # 1 个单位 0 = ratio[v] 个 v
    inv_ratio = [1] * n

    def dfs(u, parent):
        for v, mul, inv in g[u]:
            if v != parent:
                ratio[v] = ratio[u] * mul % MOD
                inv_ratio[v] = inv_ratio[u] * inv % MOD
                dfs(v, u)

    dfs(0, -1)
    return [ratio[b] * inv_ratio[a] % MOD
            for a, b in queries]
```

**复杂度。** 时间 `O(n+q)`，空间 `O(n)`。

**易错点。**
- 当整数除法：结果是分数，只能在模意义下乘逆元，`1/2` 对应 `500000004`。
- 反向边忘了取逆元：`1` 个 `target` 是 `1/factor` 个 `source`。
- 链状树 `n=10^5`：递归超过 CPython 默认上限，`RecursionError`。

**追问。**
- 递归太深怎么办？：改 BFS，出队时更新未访问邻居，逻辑一致。
- 图里有环或冗余边（LC 399）？：遇到已访问的点顺便校验比值是否一致。

**同模式。** LC 399 除法求值、LC 990 等式方程的可满足性、LC 2316 统计无向图中无法互相到达点对数
