---
id: tlc-construct-binary-tree-from-preorder-and-postorder-traversal-2-code
node: a.construct-binary-tree-from-preorder-and-postorder-traversal
type: qa
step: 2
---
## Q
**LC 889 从前序与后序遍历序列构造二叉树**｜写出 Python 实现

`preorder` 与 `postorder` 是同一棵无重复值二叉树的前序与后序（长度 `1..30`，值各自互不相同，保证来自同一棵树）；返回任意一棵满足条件的二叉树。

## A
**思路。** 前序首元素是根；若 `size > 1`，前序第二个元素是左子树的根，它在后序里的下标决定左子树大小。递归时只传 `(pre_lo, post_lo, size)`，用预建的字典 `post_idx` 做 `O(1)` 查找。

```python
def construct_from_pre_post(preorder: list[int], postorder: list[int]) -> TreeNode | None:
    post_idx = {v: i for i, v in enumerate(postorder)}   # 值 -> 它在后序里的下标，O(1) 查左子树大小

    def build(pre_lo: int, post_lo: int, size: int) -> TreeNode | None:
        if size == 0:
            return None
        root = TreeNode(preorder[pre_lo])
        if size == 1:
            return root
        left_root = preorder[pre_lo + 1]                 # 前序里根后面紧跟的是左子树的根
        left_size = post_idx[left_root] - post_lo + 1    # 后序里左子树根是左子树的最后一个
        root.left = build(pre_lo + 1, post_lo, left_size)
        root.right = build(pre_lo + 1 + left_size, post_lo + left_size, size - 1 - left_size)
        return root

    return build(0, 0, len(preorder))
```

运行：`[1,2,4,5,3,6,7]`、`[4,5,2,6,7,3,1]` → 层序 `[1,2,3,4,5,6,7]`；`[1]`、`[1]` → `[1]`；`[1,2]`、`[2,1]` → `[1,2]`；`[1,2,3]`、`[3,2,1]` → `[1,2,null,3]`。重建后树的前序、后序都与输入一致。

**复杂度。** 时间 `O(n)`：每个结点建一次、每次字典查找 `O(1)`；空间 `O(n)`：字典加递归栈（最坏深度 `n <= 30`）。

**写法要点。** 字典推导式 `{v: i for i, v in enumerate(postorder)}` 一行建索引；内层函数 `build` 闭包引用外层的两个数组，避免每次递归传它们；只传下标和长度而不切片，避免 `O(n)` 的拷贝；`size == 0` 与 `size == 1` 两个基准情形分开写，`size == 1` 提前返回才能安全读 `preorder[pre_lo + 1]`。
