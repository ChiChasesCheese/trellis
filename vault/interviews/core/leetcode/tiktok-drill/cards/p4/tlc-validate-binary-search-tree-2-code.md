---
id: tlc-validate-binary-search-tree-2-code
node: p4.validate-binary-search-tree
type: qa
step: 2
---
## Q
**LC 98 验证二叉搜索树**｜写出 Python 实现

给二叉树根结点 `root`（结点数 `1..10^4`，值在 `int32` 范围内），判断是否是有效的 BST（左子树严格小于、右子树严格大于）。要求不会因为深树而递归溢出。

## A
**思路。** 迭代中序遍历：一路向左压栈，弹出一个结点就和 `prev` 比较，要求严格递增；然后转向右子树。`prev` 初值用 `None`，避开 `int32` 边界值。

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    stack: list[TreeNode] = []
    prev: int | None = None            # 中序序列里的前一个值
    node = root
    while stack or node:
        while node:                    # 一路向左压栈
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and node.val <= prev:   # 中序必须严格递增
            return False
        prev = node.val
        node = node.right
    return True
```

运行：`[2,1,3]` → `True`，`[5,1,4,null,null,3,6]` → `False`，`[1,1]` → `False`，单个结点 `[2147483647]` → `True`，`None` → `True`；`10^4` 个结点的右斜链（值 `0..9999`）→ `True`，没有递归溢出。

**复杂度。** 时间 `O(n)`：每个结点入栈、出栈各一次；空间 `O(h)`：栈里最多存一条从根往下的路径，链状树时是 `O(n)`。

**写法要点。** `while stack or node` 同时覆盖「还有待处理的右子树」和「还有等着访问的祖先」。`prev: int | None` 用 `None` 表示「还没访问过任何结点」，比 `-inf` 或 `-2**31` 都稳，值域本身就是 `int32`。发现违规立刻 `return False`，不必遍历完。`TreeNode | None` 是 3.10+ 的联合类型写法，不需要 `Optional`。
