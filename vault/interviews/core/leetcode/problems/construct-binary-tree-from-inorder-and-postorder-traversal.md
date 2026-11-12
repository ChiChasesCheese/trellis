---
slug: construct-binary-tree-from-inorder-and-postorder-traversal
---
## Q
**LC 106 从中序与后序遍历序列构造二叉树**｜Medium

给同一棵二叉树（值互不相同）的中序和后序遍历，还原这棵树。

## A
**一句话。** 后序的最后一个是根，在中序里一分为二；后序倒着读是「根、右、左」，所以先建右子树。

```python
def build_tree(inorder, postorder):
    idx = {v: i for i, v in enumerate(inorder)}
    post = list(postorder)

    def build(lo, hi):             # 中序区间 inorder[lo:hi]
        if lo >= hi:
            return None
        root = TreeNode(post.pop())
        mid = idx[root.val]
        root.right = build(mid + 1, hi)   # 先右后左
        root.left = build(lo, mid)
        return root

    return build(0, len(inorder))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先建左子树：会把右子树的根错当成左子树的根，树建错。
- 对 `postorder` 原地 `pop`：改了调用者的数据，要先复制。

**追问。**
- 左链状树深 `3000` 会怎样？：超过 CPython 递归上限，调高上限或改迭代。
- 先序加后序能还原吗？：不唯一，只有一个孩子时分不清左右（LC 889）。

**同模式。** LC 105 从前序与中序遍历序列构造二叉树、LC 889 从前序与后序遍历序列构造二叉树、LC 654 最大二叉树、LC 108 将有序数组转换为二叉搜索树
