---
slug: binary-tree-longest-consecutive-sequence
---
## Q
**LC 298 二叉树最长连续序列**｜Medium

求二叉树中自上而下、每步恰好递增 `1` 的最长路径的节点数（可从任意节点开始）。

## A
**一句话。** 自顶向下 DFS，把「以当前节点结尾的连续长度」往下传，子值等于父值加一就加一，否则重置为 `1`。

```python
def longest_consecutive(root):
    best = 0

    def dfs(node, length):
        nonlocal best
        best = max(best, length)
        for child in (node.left, node.right):
            if child:
                ok = child.val == node.val + 1
                dfs(child, length + 1 if ok else 1)

    if root:
        dfs(root, 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 条件写成 `abs(child.val - node.val) == 1`：把递减也算上，`[2,null,3,2,null,1]` 得 `4`，应为 `2`。
- 不满足时忘了重置为 `1`：长度一直累加，答案偏大。
- 链状树有 `30000` 层：递归超过 CPython 默认上限，要调高或改显式栈。

**追问。**
- 路径可递增也可递减、能拐弯（LC 549）？：后序遍历，每个节点返回向下最长递增链和递减链，拐点处合并 `inc + dec - 1`。

**同模式。** LC 549 二叉树中最长的连续序列、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 543 二叉树的直径
