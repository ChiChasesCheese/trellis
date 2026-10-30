---
id: tlc-validate-binary-search-tree-2-code
node: p4.validate-binary-search-tree
type: qa
step: 2
---
## Q
**LC 98 验证二叉搜索树**｜写出 Python 实现

给二叉树根结点 `root`（结点数 `1..10^4`，值在 `int32` 范围内），判断是否是有效的 BST（左子树严格小于、右子树严格大于）。主解法用递归即可。

## A
**思路。** 递归中序遍历：先左子树，再和 `prev` 比较，要求严格递增，最后右子树；左子树一失败就一路返回 `False`。`prev` 初值用 `None`，避开 `int32` 边界值。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    prev: int | None = None            # 中序序列里的前一个值

    def inorder(node: TreeNode | None) -> bool:   # 这棵子树的中序是否严格递增
        nonlocal prev
        if node is None:
            return True
        if not inorder(node.left):     # 左子树先走完；已经失败就一路返回
            return False
        if prev is not None and node.val <= prev:   # 中序必须严格递增
            return False
        prev = node.val
        return inorder(node.right)

    return inorder(root)
```

运行：`[2,1,3]` → `True`，`[5,1,4,null,null,3,6]` → `False`，`[1,1]` → `False`，单个结点 `[2147483647]` → `True`，`None` → `True`；`10^4` 个结点的右斜链（值 `0..9999`）→ `True`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个结点访问一次；空间 `O(h)`：递归栈里最多存一条从根往下的路径，链状树时是 `O(n)`。

**写法要点。** `inorder` 返回布尔值，`nonlocal prev` 让递归调用共享「上一个访问的值」；`and`/提前 `return False` 让失败立刻上传。`prev: int | None` 用 `None` 表示「还没访问过任何结点」，比 `-inf` 或 `-2**31` 都稳，值域本身就是 `int32`。发现违规立刻 `return False`，不必遍历完。`TreeNode | None` 是 3.10+ 的联合类型写法，不需要 `Optional`。
