---
id: tlc-recover-binary-search-tree-2-code
node: a.recover-binary-search-tree
type: qa
step: 2
---
## Q
**LC 99 恢复二叉搜索树**｜写出 Python 实现

给 BST 的根结点 `root`（结点数 `[2, 1000]`，`-2^31 <= Node.val <= 2^31 - 1`），其中恰好两个结点的值被交换。原地恢复，不改变树结构。主解法用 `O(n)` 额外空间即可。

## A
**思路。** 用显式栈做迭代中序遍历，保留前驱 `prev`。遇到 `prev.val > node.val` 就是一处逆序：第一次遇到时记 `first = prev`，每次遇到都更新 `second = node`。遍历完交换 `first`、`second` 的值。

```python
def recover_tree(root: TreeNode | None) -> None:
    stack: list[TreeNode] = []
    prev: TreeNode | None = None       # 中序遍历中刚访问过的前一个结点
    first = second = None              # 两个被交换的结点
    node = root
    while stack or node:
        while node:                    # 一路向左压栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出的顺序就是中序（升序）顺序
        if prev and prev.val > node.val:        # 一处逆序对
            if first is None:
                first = prev           # 第一处逆序：较大的那个是被换错的结点
            second = node              # 最后一处逆序：较小的那个是另一个
        prev = node
        node = node.right
    if first and second:
        first.val, second.val = second.val, first.val
```

运行：`[1,3,null,null,2]` → `[3,1,null,null,2]`，`[3,1,4,null,null,2]` → `[2,1,4,null,null,3]`，`[1,2]` → `[2,1]`；1000 个结点的右斜链首尾互换，恢复后值为 `0..999`，无 `RecursionError`。

**复杂度。** 时间 `O(n)`：每个结点入栈、出栈各一次；空间 `O(h)`，栈里最多一条根到叶的路径，最坏 `O(n)`。

**写法要点。** 用 `while stack or node` 的迭代中序模板，避开递归深度限制（树高可达 1000）；`first = second = None` 一行初始化两个不可变的 `None`，安全；`prev and prev.val > node.val` 先判 `prev` 非空，避开第一个结点；`first.val, second.val = second.val, first.val` 用元组交换，不需要临时变量。
