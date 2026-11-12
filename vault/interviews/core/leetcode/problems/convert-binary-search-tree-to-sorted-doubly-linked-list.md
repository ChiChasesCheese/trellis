---
slug: convert-binary-search-tree-to-sorted-doubly-linked-list
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜Medium

把 BST 原地转成排序的循环双向链表（`left` 当前驱，`right` 当后继），返回最小节点。

## A
**一句话。** 中序遍历即升序：记住上一个节点 `prev` 互相连接，最后首尾成环。

```python
def tree_to_doubly_list(root):
    if root is None:
        return None
    first = prev = None

    def inorder(node):
        nonlocal first, prev
        if node is None:
            return
        inorder(node.left)
        if prev:
            prev.right, node.left = node, prev
        else:
            first = node       # 中序第一个就是最小值
        prev = node
        inorder(node.right)    # node.right 此时还没被改

    inorder(root)
    first.left, prev.right = prev, first
    return first
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 忘了最后首尾相连：最小节点的 `left` 仍是 `None`，沿前驱走不回来。
- 改指针时机不对：`prev.right` 要等 `prev` 的右子树已读走后再改，提前改会丢右子树。
- `2000` 层右斜链：递归超过 CPython 默认上限，`RecursionError`。

**追问。**
- 只要普通双向链表？：去掉最后一行首尾连线。
- 递归太深怎么办？：迭代中序，显式栈，连接逻辑相同。

**同模式。** LC 94 二叉树的中序遍历、LC 230 二叉搜索树中第 K 小的元素、LC 114 二叉树展开为链表、LC 98 验证二叉搜索树
