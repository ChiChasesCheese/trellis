---
slug: lowest-common-ancestor-of-a-binary-tree-iv
---
## Q
**LC 1676 二叉树的最近公共祖先 IV**｜Medium

给二叉树 `root` 和一组节点 `nodes`（都在树中），返回它们的最近公共祖先。

## A
**一句话。** 经典 LCA 后序递归，把「等于 `p` 或 `q`」换成「属于目标集合」，左右都非空的节点就是答案。

```python
def lowest_common_ancestor(root, nodes):
    targets = set(nodes)

    def dfs(node):
        if not node or node in targets:
            return node           # 遇到目标就不再往下
        left, right = dfs(node.left), dfs(node.right)
        if left and right:
            return node           # 两侧都有目标：汇合点
        return left or right

    return dfs(root)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 目标集合用列表：每次 `in` 是 `O(k)`，总时间退化成 `O(nk)`。
- 遇到目标后继续往下找：目标在目标之下时会得到更深的节点，`nodes=[5,4]` 且 `4` 在 `5` 下应返回 `5`。

**追问。**
- 目标可能不在树中（LC 1644）？：再统计找到几个目标，不足就返回 `None`。
- 节点带父指针（LC 1650）？：沿父指针上走，等价于链表相交。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 1644 二叉树的最近公共祖先 II、LC 865 具有所有最深节点的最小子树
