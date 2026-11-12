---
slug: minimum-edge-reversals-so-every-node-is-reachable
---
## Q
**LC 2858 可以到达每一个节点的最少边反转次数**｜Hard

有向图去掉方向是一棵树。对每个节点 `i`，求从 `i` 出发能到达所有节点最少要反转几条边。

## A
**一句话。** 换根 DP：以 `0` 为根数出要反转的边数，换根时只有被换的那条边的朝向变，`ans[v] = ans[u] ± 1`。

```python
def min_edge_reversals(n, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append((v, 0))    # 顺着走，不用反转
        g[v].append((u, 1))    # 逆着走，要反转
    ans = [0] * n

    def count(u, p):           # 以 0 为根，边都朝外的反转数
        return sum(w + count(v, u)
                   for v, w in g[u] if v != p)

    def reroot(u, p):
        for v, w in g[u]:
            if v != p:
                # w=0 的边换根后要反转 +1；w=1 的不用了 -1
                ans[v] = ans[u] + (1 if w == 0 else -1)
                reroot(v, u)

    ans[0] = count(0, -1)
    reroot(0, -1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 换根时符号写反：示例一得 `[1,1,2,0]`，应为 `[1,1,0,2]`。
- 对每个节点各 DFS 一次：`O(n²)`，`n=10⁵` 超时。
- 链状输入有 `10⁵` 层：CPython 递归会 `RecursionError`，要调高上限或改迭代。

**追问。**
- 为什么换根只差 `±1`？：边 `(u,v)` 把树分成两侧，两侧内部边的朝向要求都不变，只有这条边自己变。
- 图里有环呢？：不再是树，要先缩点再求最小树形图，是另一道题。

**同模式。** LC 834 树中距离之和、LC 1466 重新规划路线、LC 310 最小高度树
