---
slug: minimum-absolute-difference-in-bst
---
## Q
**LC 530 二叉搜索树的最小绝对差**｜Easy

给你一个二叉搜索树的根结点 `root`，返回树中**任意两个不同结点值之差**的最小绝对值。树中结点数在 `[2, 10^4]`，`0 <= Node.val <= 10^5`。例：`root = [4,2,6,1,3]` → `1`；`root = [1,0,48,null,null,12,49]` → `1`。（与 LC 783 相同。）

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** BST 中序遍历（inorder）是升序；最小差只出现在**相邻**的两个值之间。

**一句话。** 中序遍历时记住上一个访问的值，当前值减上一个值就是一对相邻差，取最小。

**识别。** 「BST + 值之间的差 / 第 k 小 / 是否有序」= 中序遍历得到有序序列；有序序列上的最小差只看相邻对，`n = 10^4`，一次遍历 `O(n)`。

**推导。** 暴力：所有结点两两比较，`O(n^2)`。把值排好序，任意两个数的差都不会小于它们之间相邻差之和中的最小项，所以只比较相邻。BST 的中序遍历本来就是排好序的，边遍历边和上一个比较，不需要额外排序或存储。

```python
from math import inf


def get_minimum_difference(root: TreeNode | None) -> int:
    best = inf
    prev: int | None = None  # 中序遍历里上一个访问的值

    def inorder(node: TreeNode | None) -> None:
        nonlocal best, prev
        if not node:
            return
        inorder(node.left)
        if prev is not None:  # 升序序列上相邻两个值的差，一定非负
            best = min(best, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return best
```

运行：`[4,2,6,1,3]` → `1`；`[1,0,48,null,null,12,49]` → `1`；`[10,4,null,null,9]` → `1`；`[1,null,100000]` → `99999`。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈，`h` 为树高）。

**拓展优化。**
- 显式栈的迭代中序，不受递归深度限制：

```python
from math import inf


def get_minimum_difference_iter(root: TreeNode | None) -> int:
    best, prev = inf, None
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:  # 一路向左
            stack.append(node)
            node = node.left
        node = stack.pop()  # 弹出的就是中序的下一个
        if prev is not None:
            best = min(best, node.val - prev)
        prev = node.val
        node = node.right
    return best
```

**易错点。**
- 只比较父子结点：树 `[10,4,null,null,9]` 里 `10` 与 `9` 差 `1`，但它们不是父子，只比较父子会得到 `5`，正确是 `1`。
- `prev` 初值设为 `0` 而不是 `None`：树 `[1,null,100000]` 会多算一对 `1 - 0`，得到 `1`，正确是 `99999`。
- 最坏深度：树退化成 `10^4` 个结点的链时，递归深度 `10^4`，超过 CPython 默认约 `1000` 的递归上限，抛 `RecursionError`；要么 `sys.setrecursionlimit`，要么用上面的迭代版本。

**同模式。** LC 783 二叉搜索树结点最小距离、LC 98 验证二叉搜索树、LC 230 二叉搜索树中第 K 小的元素、LC 501 二叉搜索树中的众数。
