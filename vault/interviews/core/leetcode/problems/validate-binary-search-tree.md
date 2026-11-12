---
slug: validate-binary-search-tree
---
## Q
**LC 98 验证二叉搜索树**｜Medium

判断二叉树是否是有效 BST：左子树严格小于根，右子树严格大于根，子树也都是 BST。

## A
**一句话。** BST 的中序遍历严格递增，递归中序遍历并和上一个值比较，出现 `<=` 就失败。

```python
def is_valid_bst(root):
    prev = None                    # 中序的前一个值

    def inorder(node):
        nonlocal prev
        if node is None:
            return True
        if not inorder(node.left):
            return False
        if prev is not None and node.val <= prev:
            return False           # 必须严格递增
        prev = node.val
        return inorder(node.right)

    return inorder(root)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只比较节点和它的孩子：`[5,4,6,null,null,3,7]` 每个节点都合格，但 `3` 在根 `5` 的右子树里，应为 `False`。
- 用 `<` 判失败：`[1,1]` 两个值相等，应为 `False`。
- 用 `-2^31` 当 `prev` 初值：树 `[-2147483648]` 会误判，用 `None` 或 `-inf`。

**追问。**
- 自顶向下传区间怎么写？：`check(node, lo, hi)`，往左收紧上界，往右收紧下界，要求 `lo < val < hi`。
- 怕递归太深呢？：迭代中序，一路向左压栈，弹出时和 `prev` 比较。

**同模式。** LC 230 BST 中第 K 小的元素、LC 99 恢复二叉搜索树、LC 530 BST 的最小绝对差、LC 94 二叉树的中序遍历
