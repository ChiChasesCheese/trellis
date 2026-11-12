---
slug: lowest-common-ancestor-of-a-binary-search-tree
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Medium

在二叉搜索树中找两个给定节点 `p`、`q` 的最近公共祖先（节点可以是自己的祖先）。

## A
**一句话。** 两个值都比当前小就进左子树，都比当前大就进右子树，否则当前节点就是分叉点。

```python
def lowest_common_ancestor(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor(root.right, p, q)
    return root     # 分居两侧，或 root 就是其中之一
```

**复杂度。** 时间 `O(h)`，空间 `O(h)`。

**易错点。**
- 比较写成 `<=`、`>=`：`p=2, q=4` 走到 `2` 还继续进右子树，得 `3`，应为 `2`。
- 直接比较节点 `p < root`：`TreeNode` 不能比较，要比 `.val`。

**追问。**
- 不想用递归栈？：改成 `while` 循环往下走，空间 `O(1)`。
- 普通二叉树怎么做（LC 236）？：BST 的大小关系不可用，改成后序递归，左右都找到就是 `root`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 700 二叉搜索树中的搜索、LC 701 二叉搜索树中的插入操作、LC 450 删除二叉搜索树中的节点
