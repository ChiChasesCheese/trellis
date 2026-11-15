---
slug: count-pairs-of-connectable-servers-in-a-weighted-tree-network
---
## Q
**LC 3067 在带权树网络中统计可连接服务器对数目**｜Medium

`n <= 1000` 个点的带权树。若 `a`、`b` 到 `c` 的距离都能被 `signalSpeed` 整除，且两条路径没有公共边，则 `a`、`b` 通过 `c` 可连接。对每个 `c` 求可连接的点对数。

## A
**一句话。** 没有公共边就是 `a`、`b` 在 `c` 的不同分支里；以每个 `c` 为根，对每条分支 DFS 数出距离能整除的点数 `k`，不同分支两两相乘累加（边加边算 `seen·k`）。

```python
def count_pairs_of_connectable_servers(edges, signal_speed):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b, w in edges:
        g[a].append((b, w))
        g[b].append((a, w))

    def dfs(u, fa, d):         # 这一支里距离能整除的点数
        cnt = int(d % signal_speed == 0)
        for v, w in g[u]:
            if v != fa:
                cnt += dfs(v, u, d + w)
        return cnt

    ans = [0] * n
    for c in range(n):
        seen = 0               # 之前各分支的点数之和
        for v, w in g[c]:
            k = dfs(v, c, w)
            ans[c] += seen * k  # 与之前的分支两两配对
            seen += k
    return ans
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 把所有分支的点数加总后算 `C(total, 2)`：同一分支里的两点会共用 `c` 出发的边。
- 把 `c` 自己也算进去：`c` 的距离是 0 能整除，但题目要求 `a, b != c`，所以从邻居开始数。

**追问。**
- 不同分支两两相乘怎么 `O(度数)` 算？：维护已处理分支的总数 `seen`，新分支贡献 `seen·k`。
- `n` 到 `10^5`？：要换根 DP 维护每个点各分支里「距离模 `signalSpeed`」的计数，较复杂。

**同模式。** LC 543 二叉树的直径、LC 2867 统计树中的合法路径数目
