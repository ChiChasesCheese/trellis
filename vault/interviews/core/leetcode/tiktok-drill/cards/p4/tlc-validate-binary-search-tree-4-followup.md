---
id: tlc-validate-binary-search-tree-4-followup
node: p4.validate-binary-search-tree
type: qa
step: 4
---
## Q
**LC 98 验证二叉搜索树**｜追问

面试官接着问：（1）不用中序，自顶向下带区间怎么写？（2）如果允许重复值（左子树可以 `<=` 当前值）呢？（3）要求 `O(1)` 额外空间？

## A
1. **自顶向下带区间**：每个结点必须落在一个开区间 `(lo, hi)` 内；进左子树把上界收紧到当前值，进右子树把下界收紧到当前值。同样用显式栈，结点数 `10^4` 的链状树也不会溢出：

```python
from math import inf


def is_valid_bst_bounds(root: TreeNode | None) -> bool:
    stack = [(root, -inf, inf)]            # (结点, 开区间下界, 开区间上界)
    while stack:
        node, lo, hi = stack.pop()
        if node is None:
            continue
        if not lo < node.val < hi:
            return False
        stack.append((node.left, lo, node.val))     # 左子树必须 < 当前值
        stack.append((node.right, node.val, hi))    # 右子树必须 > 当前值
    return True
```

2. **允许重复**：先问清重复值放哪一边。规定「左子树 `<=` 当前值」时，左边界是闭的：结点检查改成 `lo < val <= hi`，往左走时 `hi` 取当前值，往右走时 `lo` 取当前值（右边仍严格大于）。中序版本则把失败条件从 `val <= prev` 改成 `val < prev`。
3. **`O(1)` 空间**：莫里斯遍历（Morris traversal）临时改指针，把前驱的右指针指回当前结点，借此不用栈完成中序；每个结点只访问常数次，仍是 `O(n)` 时间，遍历完要把指针还原。面试里知道它存在、能说出原理即可。

**Python 提醒**：`-inf` / `inf` 是 `float`，和 `int` 比较没问题且不会溢出，但类型标注上区间是 `float | int`；用 `lo < node.val < hi` 的链式比较比 `lo < node.val and node.val < hi` 更清楚，也只计算一次 `node.val`。
