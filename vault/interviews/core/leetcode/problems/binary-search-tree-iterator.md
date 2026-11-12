---
slug: binary-search-tree-iterator
---
## Q
**LC 173 二叉搜索树迭代器**｜Medium

实现 BST 中序遍历的迭代器 `BSTIterator`：`next()` 返回下一个更大的数（首次是最小值），`hasNext()` 判断是否还有数。

## A
**一句话。** 构造时中序遍历把值收进升序列表，`next` 和 `hasNext` 只移动一个下标。

```python
class BSTIterator:
    def __init__(self, root):
        self.vals = []

        def inorder(node):
            if node:
                inorder(node.left)
                self.vals.append(node.val)   # 中序即升序
                inorder(node.right)

        inorder(root)
        self.i = -1                          # 在最小值之前

    def next(self):
        self.i += 1
        return self.vals[self.i]

    def hasNext(self):
        return self.i + 1 < len(self.vals)
```

**复杂度。** 时间 构造 `O(n)`、`next` 与 `hasNext` 各 `O(1)`，空间 `O(n)`。

**易错点。**
- `hasNext` 写成 `self.i < len(self.vals)`：取完最后一个数后仍返回 `True`，要 `self.i + 1 < len`。
- 退化成 `10^5` 个结点的链：递归中序超过 CPython 默认递归上限，会 `RecursionError`。

**追问。**
- 只能用 `O(h)` 内存怎么办？：栈里存当前结点的左链，`next` 弹出结点后把其右子树的左链压栈，均摊 `O(1)`。
- 栈版本最容易漏什么？：弹出后忘了压右子树的左链，`[7,3,15,null,null,9,20]` 弹出 `3`、`7` 后栈就空了。

**同模式。** LC 94 二叉树的中序遍历、LC 230 二叉搜索树中第 K 小的元素、LC 98 验证二叉搜索树、LC 284 窥视迭代器
