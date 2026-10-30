---
id: tlc-lowest-common-ancestor-of-deepest-leaves-2-code
node: b.lowest-common-ancestor-of-deepest-leaves
type: qa
step: 2
---
## Q
**LC 1123 最深叶节点的最近公共祖先**｜Medium · 字节高频｜写出 Python 实现

二叉树的根结点 `root`（结点数 `1` 到 `1000`，值互不相同）。返回最深叶结点们的最近公共祖先结点。要求 `O(n)`。

## A
**思路。** 后序递归：`dfs(node)` 返回 `(最深叶深度, 该深度叶子的 LCA)`，从两个孩子的返回值合并：左右一样深就返回自己，否则取更深那一边。根的返回值里的 LCA 就是答案。

```python
def lca_deepest_leaves(root: TreeNode | None) -> TreeNode | None:
    def dfs(node: TreeNode | None) -> tuple[int, TreeNode | None]:
        # 返回 (node 子树里最深叶子的深度（以 node 为 1）, 这些最深叶子的最近公共祖先)
        if node is None:
            return 0, None                     # 空子树
        ld, lca_l = dfs(node.left)
        rd, lca_r = dfs(node.right)
        if ld > rd:
            return ld + 1, lca_l               # 最深的叶子都在左边
        if rd > ld:
            return rd + 1, lca_r               # 最深的叶子都在右边
        return ld + 1, node                    # 左右一样深（含叶子本身）：node 就是汇合点

    return dfs(root)[1]
```

运行（返回结点的值）：`[3,5,1,6,2,0,8,null,null,7,4]` → `2`，`[1]` → `1`，`[0,1,3,null,2]` → `2`，`[1,2,3]` → `1`，`[1,2,null,3]` → `3`；`1000` 个结点的链状树 → `999`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`；空间 `O(h)`：递归栈，链状树时为 `O(n)`。

**写法要点。** `dfs` 返回二元组，一次递归同时带回深度和答案，不需要两遍；`ld, lca_l = dfs(node.left)` 元组解包一次拿到两个量；空子树返回 `(0, None)`，叶子的 `ld == rd == 0`，自然走「一样深」分支返回自己；`dfs(root)[1]` 只取答案。
