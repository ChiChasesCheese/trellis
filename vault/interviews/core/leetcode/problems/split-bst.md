---
slug: split-bst
---
## Q
**LC 776 拆分二叉搜索树**｜Medium

给定 BST 和 `target`，把它拆成两棵 BST：一棵所有值 `<= target`，另一棵所有值 `> target`，尽量保持原有的父子结构，返回两棵树的根。

## A
**一句话。** 递归：根 `<= target` 时根和左子树都属于小树，只需拆右子树，把拆出的小部分接回根的右边；根 `> target` 时对称处理左子树。

```python
def split_bst(root, target):
    if root is None:
        return [None, None]
    if root.val <= target:
        # 根与左子树都 <= target：只拆右子树
        small, large = split_bst(root.right, target)
        root.right = small
        return [root, large]
    small, large = split_bst(root.left, target)
    root.left = large          # 对称：只拆左子树
    return [small, root]
```

**复杂度。** 时间 `O(h)`，空间 `O(h)`。

**易错点。**
- 拆完右子树后把 `large` 接回根：大于 `target` 的部分应独立成另一棵树，接回的是 `small`。
- 中序遍历后重新建树：结构会变，也不是 `O(h)`。

**追问。**
- 为什么只走一条路径？：每层只需拆一个子树，另一个子树整体归属已经确定。
- 和 Treap 的 `split` 一样吗？：完全相同，平衡树按键拆分就是这样写的，配合 `merge` 能做区间操作。

**同模式。** LC 98 验证二叉搜索树、LC 450 删除二叉搜索树中的节点、LC 669 修剪二叉搜索树
