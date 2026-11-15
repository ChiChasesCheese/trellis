---
slug: maximize-the-number-of-target-nodes-after-connecting-trees-i
---
## Q
**LC 3372 连接两棵树后最大目标节点数目 I**｜Medium

两棵树（各 `<= 1000` 个点）。与 `u` 距离不超过 `k` 的点是 `u` 的目标节点（含自己）。对第一棵树的每个点 `i`，可以在两棵树间任连一条边（各问独立），求 `i` 的目标节点数的最大值。

## A
**一句话。** 新边自己占 1 步，所以答案 = 树 1 中距 `i` 不超过 `k` 的点数 + 树 2 中「距某点不超过 `k-1` 的点数」的最大值（把边连到 `i` 和那个点上）；两部分都从每个点 DFS 数一遍。

```python
def max_target_nodes(edges1, edges2, k):
    def build(edges):
        g = [[] for _ in range(len(edges) + 1)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)
        return g

    def count(g, u, fa, d):    # 距 u 不超过 d 的点数
        if d < 0:
            return 0
        return 1 + sum(count(g, v, u, d - 1)
                       for v in g[u] if v != fa)

    g1, g2 = build(edges1), build(edges2)
    best2 = max(count(g2, v, -1, k - 1)
                for v in range(len(g2)))
    return [count(g1, u, -1, k) + best2
            for u in range(len(g1))]
```

**复杂度。** 时间 `O(n² + m²)`，空间 `O(n + m)`。

**易错点。**
- 树 2 也用 `k`：跨过新边要花 1 步，树 2 那边只剩 `k-1`。
- `k = 0` 时树 2 贡献 1：只有 `i` 自己，`d < 0` 返回 0 正好处理。

**追问。**
- 为什么树 2 的部分与 `i` 无关？：新边的一端可以直接连在 `i` 上，最优就是树 2 里那个最好的点，对所有 `i` 都一样。
- 改成「距离为偶数」？：那是 II 版，按二分图染色，答案只与颜色有关，`O(n + m)`。

**同模式。** LC 102 二叉树的层序遍历、LC 863 二叉树中所有距离为 K 的结点、LC 3373 连接两棵树后最大目标节点数目 II
