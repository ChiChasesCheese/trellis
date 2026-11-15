---
slug: lowest-common-ancestor-of-a-binary-tree-ii
---
## Q
**LC 1644 二叉树的最近公共祖先 II**｜Medium

给二叉树根 `root` 和结点 `p`、`q`，求它们的最近公共祖先。`p` 或 `q` 可能不在树中，此时返回 `None`。

## A
**一句话。** 后序统计每棵子树里命中了几个目标，第一个计数到 2 的结点就是答案；必须扫完整棵树，才能确认两个目标都存在。

```python
def lowest_common_ancestor(root, p, q):
    ans = None
    def dfs(node):               # 返回子树里命中的目标数
        nonlocal ans
        if not node:
            return 0
        cnt = dfs(node.left) + dfs(node.right)
        cnt += (node is p) + (node is q)
        if cnt == 2 and ans is None:
            ans = node           # 后序：最先凑够 2 的最深
        return cnt
    dfs(root)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 沿用 LC 236 的写法见到 `p` 就返回：若 `q` 不在树里，会把 `p` 当成答案。
- 命中 `p` 后不再往下搜：`q` 在 `p` 下面时漏计。

**追问。**
- 一遍遍历怎么做到？：这里就是一遍；LC 236 的版本遇到目标就提前返回，因此无法验证另一个是否存在。
- 有父指针时呢？：沿 `p` 向上记下所有祖先，再从 `q` 向上找第一个出现过的。

**同模式。** LC 236 二叉树的最近公共祖先、LC 1676 二叉树的最近公共祖先 IV、LC 1650 二叉树的最近公共祖先 III、LC 235 二叉搜索树的最近公共祖先
