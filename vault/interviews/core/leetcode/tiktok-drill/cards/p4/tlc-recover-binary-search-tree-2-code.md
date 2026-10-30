---
id: tlc-recover-binary-search-tree-2-code
node: p4.recover-binary-search-tree
type: qa
step: 2
---
## Q
**LC 99 恢复二叉搜索树**｜写出 Python 实现

给 BST 的根结点 `root`（结点数 `[2, 1000]`，`-2^31 <= Node.val <= 2^31 - 1`），其中恰好两个结点的值被交换。原地恢复，不改变树结构。主解法用 `O(n)` 额外空间即可。

## A
**思路。** 递归中序遍历（左、处理、右），保留前驱 `prev`。遇到 `prev.val > node.val` 就是一处逆序：第一次遇到时记 `first = prev`，每次遇到都更新 `second = node`。遍历完交换 `first`、`second` 的值。

```python
def recover_tree(root: TreeNode | None) -> None:
    prev: TreeNode | None = None       # 中序遍历中刚访问过的前一个结点
    first = second = None              # 两个被交换的结点

    def inorder(node: TreeNode | None) -> None:
        nonlocal prev, first, second
        if node is None:
            return
        inorder(node.left)
        if prev and prev.val > node.val:        # 一处逆序对
            if first is None:
                first = prev           # 第一处逆序：较大的那个是被换错的结点
            second = node              # 最后一处逆序：较小的那个是另一个
        prev = node
        inorder(node.right)

    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val
```

运行：`[1,3,null,null,2]` → `[3,1,null,null,2]`，`[3,1,4,null,null,2]` → `[2,1,4,null,null,3]`，`[1,2]` → `[2,1]`；1000 个结点的右斜链首尾互换，恢复后值为 `0..999`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个结点访问一次；空间 `O(h)`，递归栈里最多一条根到叶的路径，最坏 `O(n)`。

**写法要点。** `inorder` 是嵌套函数，用 `nonlocal` 改写外层的 `prev`、`first`、`second`，不需要把状态当参数传来传去；`first = second = None` 一行初始化两个不可变的 `None`，安全；`prev and prev.val > node.val` 先判 `prev` 非空，避开第一个结点；`first.val, second.val = second.val, first.val` 用元组交换，不需要临时变量。
