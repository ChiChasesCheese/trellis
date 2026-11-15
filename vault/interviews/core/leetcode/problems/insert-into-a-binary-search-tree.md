---
slug: insert-into-a-binary-search-tree
---
## Q
**LC 701 二叉搜索树中的插入操作**｜Medium

向二叉搜索树插入一个不重复的值，返回插入后的根（任意合法结果都可以）。

## A
**一句话。** 按 BST 性质往下找：小于根走左、大于根走右，走到空位就新建结点挂上去，递归返回值负责接线。

```python
def insert_into_bst(root, val):
    if root is None:
        return TreeNode(val)   # 空位：新结点放这里
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
```

**复杂度。** 时间 `O(h)`，空间 `O(h)`。

**易错点。**
- 递归结果不赋回 `root.left` / `root.right`：新结点建出来了却没接到树上。
- 空树时返回原来的 `root`：应返回新结点。

**追问。**
- 迭代写法？：用指针找到最后一个非空结点，再按大小挂左或右，`O(1)` 空间。
- 插入后保持平衡？：AVL 或红黑树在回溯路径上旋转，保证 `h = O(log n)`。

**同模式。** LC 98 验证二叉搜索树、LC 450 删除二叉搜索树中的节点、LC 700 二叉搜索树中的搜索
