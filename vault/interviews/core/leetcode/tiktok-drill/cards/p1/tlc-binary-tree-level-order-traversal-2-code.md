---
id: tlc-binary-tree-level-order-traversal-2-code
node: p1.binary-tree-level-order-traversal
type: qa
step: 2
---
## Q
**LC 102 二叉树的层序遍历**｜写出 Python 实现

二叉树根节点 `root`，节点数 `[0, 2000]`，节点值 `-1000 <= Node.val <= 1000`。返回逐层从左到右的节点值，每层一个列表。

## A
**思路。** 队列里先放根。每一轮外层循环处理一整层：先读出此刻队列的长度 `len(queue)`，恰好弹出这么多个节点，把它们的值收进 `level`，同时把孩子入队。孩子属于下一层，下一轮才会被处理。

```python
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    queue = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):     # 先固定本层的节点数，循环里新入队的是下一层
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
```

运行：`[3,9,20,null,null,15,7]` → `[[3], [9, 20], [15, 7]]`，`[1]` → `[[1]]`，`[]` → `[]`，2000 个节点的单链树 → 2000 层。

**复杂度。** 时间 `O(n)`：每个节点入队、出队各一次；空间 `O(w)`，`w` 为最宽一层的节点数。

**写法要点。** `collections.deque` 的 `popleft` 是 `O(1)`，列表的 `pop(0)` 是 `O(n)`；`range(len(queue))` 只在循环开始时求值一次，循环里队列变长也不影响次数；`for _ in ...` 表示不使用循环变量；`deque([root])` 一步建好并放入根。`if node.left:` 利用节点对象默认为真、`None` 为假。
