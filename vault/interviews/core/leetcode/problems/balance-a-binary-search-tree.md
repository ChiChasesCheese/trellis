---
slug: balance-a-binary-search-tree
---
## Q
**LC 1382 将二叉搜索树变平衡**｜Medium

给一棵二叉搜索树，返回一棵节点值相同的平衡二叉搜索树（任意节点两棵子树高度差不超过 1）。

## A
**一句话。** 中序遍历得到有序数组，每次取中点作根，左右两半递归建树，高度自然平衡。

```python
def balance_bst(root):
    vals = []
    def inorder(node):
        if node:
            inorder(node.left)
            vals.append(node.val)      # 中序：有序
            inorder(node.right)
    inorder(root)
    def build(l, r):                   # 用 vals[l..r] 建树
        if l > r:
            return None
        m = (l + r) // 2               # 中点作根
        return TreeNode(vals[m], build(l, m - 1),
                        build(m + 1, r))
    return build(0, len(vals) - 1)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 想通过旋转修补原树：可行（AVL / DSW 算法）但复杂，重建更简单。
- 不用中序：直接取前序或层序会丢失 BST 的有序性。
- 中点选 `(l + r) // 2` 或 `+1` 都可以：两边至多差一个，高度差不超过 1。

**追问。**
- 想要 `O(1)` 额外空间？：Day–Stout–Warren 算法，先转成右链再分段旋转。
- 有序链表怎么建平衡 BST？：快慢指针找中点，或中序模拟边遍历边建，见 LC 109。

**同模式。** LC 108 将有序数组转换为二叉搜索树、LC 109 有序链表转换二叉搜索树、LC 110 平衡二叉树、LC 94 二叉树的中序遍历
