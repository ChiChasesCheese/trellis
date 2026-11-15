---
slug: binary-tree-longest-consecutive-sequence-ii
---
## Q
**LC 549 二叉树最长连续序列 II**｜Medium

路径可以先上后下（经过某个结点的两个孩子），每步值恰好加 1 或每步恰好减 1。求最长这样的路径的结点数。

## A
**一句话。** 后序给每个结点返回「向下连续递增的最长、向下连续递减的最长」；经过该结点的路径长是 `inc + dec - 1`。

```python
def longest_consecutive(root):
    best = 0
    def dfs(node):       # 返回 (向下递增最长, 向下递减最长)
        nonlocal best
        if not node:
            return 0, 0
        inc = dec = 1
        for kid in (node.left, node.right):
            if not kid:
                continue
            ki, kd = dfs(kid)
            if kid.val == node.val + 1:
                inc = max(inc, ki + 1)
            if kid.val == node.val - 1:
                dec = max(dec, kd + 1)
        best = max(best, inc + dec - 1)   # 递增接递减，根算一次
        return inc, dec
    dfs(root)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- `inc + dec` 不减 1：结点 `node` 被两段各算了一次。
- `inc`、`dec` 初值写成 `0`：单个结点本身就是长度为 1 的路径。
- 路径只向下：这里允许拐过某个结点，必须在结点处合并两侧。

**追问。**
- 和 LC 298 有何区别？：LC 298 只能向下且只递增，一个数就够；这里多了递减并允许拐弯，所以要两个数。
- 值相差 1 且不要求单调呢？：路径会上下振荡，这是另一类问题，需要更强约束才有解。

**同模式。** LC 298 二叉树最长连续序列、LC 124 二叉树中的最大路径和、LC 543 二叉树的直径、LC 1372 二叉树中的最长交错路径
