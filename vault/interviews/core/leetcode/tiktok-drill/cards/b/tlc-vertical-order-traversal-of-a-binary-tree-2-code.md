---
id: tlc-vertical-order-traversal-of-a-binary-tree-2-code
node: b.vertical-order-traversal-of-a-binary-tree
type: qa
step: 2
---
## Q
**LC 987 二叉树的垂序遍历**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 1000]`，`0 <= Node.val <= 1000`），根在 `(0, 0)`，左孩子 `(row + 1, col - 1)`，右孩子 `(row + 1, col + 1)`。返回垂序遍历：从最左列到最右列，每列内先按行从上到下，同行同列按值从小到大。

## A
**思路。** 用栈遍历整棵树，记录 `(col, row, val)`。整体排序后，同一列的节点连续出现；`groupby` 按列号切段，每段取出值列表。

```python
from itertools import groupby
from operator import itemgetter


def vertical_traversal(root: TreeNode | None) -> list[list[int]]:
    nodes: list[tuple[int, int, int]] = []
    stack = [(root, 0, 0)]                           # (节点, 行, 列)
    while stack:
        node, row, col = stack.pop()
        nodes.append((col, row, node.val))
        if node.left:
            stack.append((node.left, row + 1, col - 1))
        if node.right:
            stack.append((node.right, row + 1, col + 1))
    nodes.sort()                                     # 先按列、再按行、最后按值：正好是题目要的三级顺序
    return [[v for _, _, v in grp] for _, grp in groupby(nodes, key=itemgetter(0))]
```

运行：`[3,9,20,null,null,15,7]` → `[[9], [3, 15], [20], [7]]`；`[1,2,3,4,5,6,7]` → `[[4], [2], [1, 5, 6], [3], [7]]`；`[1,2,3,4,6,5,7]` → `[[4], [2], [1, 5, 6], [3], [7]]`；`1000` 个节点的斜链 → `1000` 列。

**复杂度。** 时间 `O(n log n)`：遍历 `O(n)`，排序 `O(n log n)`；空间 `O(n)`。

**写法要点。** 元组排序天然实现多级键，不需要写 `key=` 或比较函数；`itemgetter(0)` 比 `lambda t: t[0]` 更快也更清晰；`groupby` 要求相同的键**相邻**，所以必须先排序；遍历顺序（先左后右、先右后左）不影响结果，因为排序会重排。
