---
slug: maximum-sum-bst-in-binary-tree
---
## Q
**LC 1373 二叉搜索子树的最大键值和**｜Hard

在二叉树中找一棵是二叉搜索树的子树，使其键值和最大，返回该和（都为负则返回 `0`）。节点数到 `4·10^4`。

## A
**一句话。** 后序遍历，每个节点向上报「子树最小值、最大值、和」，满足 `左最大 < 根 < 右最小` 才是 BST；不是就报一组让祖先必然失败的哨兵。

```python
def max_sum_bst(root):
    ans = 0

    def dfs(node):             # 返回 (最小值, 最大值, 和)
        nonlocal ans
        if node is None:
            return inf, -inf, 0
        lmin, lmax, ls = dfs(node.left)
        rmin, rmax, rs = dfs(node.right)
        x = node.val
        if not lmax < x < rmin:
            return -inf, inf, 0    # 不是 BST，祖先也不会是
        s = ls + rs + x
        ans = max(ans, s)
        return min(lmin, x), max(rmax, x), s

    dfs(root)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 空树返回 `(0, 0, 0)`：叶子的判断 `0 < x < 0` 失败；空树要 `(inf, -inf)`。
- 返回 `max(lmax, x)`：右子树才有最大值，要 `max(rmax, x)`，空右子树时 `rmax = -inf` 正好得 `x`。

**追问。**
- 链状树深 `4·10^4`？：调大递归上限，或迭代后序把结果存字典。
- 只问最大 BST 子树的节点数（LC 333）？：把和换成节点数。

**同模式。** LC 98 验证二叉搜索树、LC 124 二叉树中的最大路径和、LC 333 最大二叉搜索子树
