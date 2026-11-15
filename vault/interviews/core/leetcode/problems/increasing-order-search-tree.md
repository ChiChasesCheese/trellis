---
slug: increasing-order-search-tree
---
## Q
**LC 897 递增顺序搜索树**｜Easy

给一棵二叉搜索树，把它改成「递增顺序」：中序遍历的第一个结点是新的根，所有结点都没有左孩子，只有一个右孩子。

## A
**一句话。** 中序遍历，把当前结点接到链尾 `tail.right`，同时清掉它的左孩子，原地改指针。

```python
def increasing_bst(root):
    dummy = tail = TreeNode()
    def dfs(node):
        nonlocal tail
        if not node:
            return
        dfs(node.left)
        node.left = None             # 中序位置：当前结点接到链尾
        tail.right = node
        tail = node
        dfs(node.right)
    dfs(root)
    return dummy.right
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈）。

**易错点。**
- 忘了 `node.left = None`：结点还挂着原来的左子树，成了环或多余的分支。
- 先递归右子树：中序必须是左、根、右，顺序错了链就倒过来。

**追问。**
- 不改原树怎么办？：先中序收集值，再顺着新建一条右链，空间 `O(n)`。
- 想要 `O(1)` 额外空间？：Morris 中序遍历，边遍历边改指针。

**同模式。** LC 114 二叉树展开为链表、LC 426 将二叉搜索树转化为排序的双向链表、LC 94 二叉树的中序遍历
