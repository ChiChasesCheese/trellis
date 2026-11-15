---
slug: restore-the-array-from-adjacent-pairs
---
## Q
**LC 1743 从相邻元素对还原数组**｜Medium

有一个元素互不相同的整数数组 `nums`，给出它所有相邻元素对 `adjacentPairs`（顺序任意，每对可能是 `[u, v]` 或 `[v, u]`）。还原 `nums`，答案不唯一时返回任意一个。

## A
**一句话。** 把每对当成无向边，数组就是一条链；度为 `1` 的端点是头，从它顺着邻居走到底。

```python
def restore_array(adjacent_pairs):
    g = defaultdict(list)
    for u, v in adjacent_pairs:
        g[u].append(v)
        g[v].append(u)
    # 链的两个端点只有一个邻居
    head = next(x for x in g if len(g[x]) == 1)
    res, prev = [head], None
    while len(res) <= len(adjacent_pairs):
        cur = res[-1]
        nxt = g[cur][0] if g[cur][0] != prev else g[cur][-1]
        prev = cur
        res.append(nxt)
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `g[cur][0]` 又不排除 `prev`：会在两个点之间来回走。
- 只有一对时：两个点度都是 `1`，任取一个作头都对。

**追问。**
- 为什么端点度为 `1`？：中间元素各有前后两个邻居，只有首尾只出现在一对里。

**同模式。** LC 1296 划分数组为连续数字的集合、LC 659 分割数组为连续子序列、LC 128 最长连续序列、LC 2096 从二叉树一个节点到另一个节点每一步的方向
