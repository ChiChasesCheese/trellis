---
slug: lowest-common-ancestor-of-deepest-leaves
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium

返回二叉树中所有最深叶节点的最近公共祖先。

## A
**一句话。** 后序递归返回（最深深度，其最近公共祖先），左右一样深则答案是当前节点，否则沿用更深的一侧。

```python
def lca_deepest_leaves(root):
    def dfs(node):      # 返回 (最深叶深度, 它们的 LCA)
        if node is None:
            return 0, None
        ld, lca_l = dfs(node.left)
        rd, lca_r = dfs(node.right)
        if ld > rd:
            return ld + 1, lca_l
        if rd > ld:
            return rd + 1, lca_r
        return ld + 1, node     # 一样深（含叶子本身）：汇合点

    return dfs(root)[1]
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 平局时沿用左边的答案：`[1,2,3]` 得节点 `2`，应为根 `1`，两片最深叶子分居两侧。
- 返回最深叶子的父节点：`[0,1,3,null,2]` 得节点 `1`，应为节点 `2`，只有一片最深叶子时它自己就是 LCA。

**追问。**
- 为什么平局就是当前节点？：左右最深叶子都在其下且分居两侧，再往下任一侧都盖不住另一侧。
- 任意一组节点的 LCA（LC 1676）？：后序统计子树里命中的目标数，首次凑齐总数的位置就是答案。

**同模式。** LC 865 具有所有最深节点的最小子树、LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 543 二叉树的直径
