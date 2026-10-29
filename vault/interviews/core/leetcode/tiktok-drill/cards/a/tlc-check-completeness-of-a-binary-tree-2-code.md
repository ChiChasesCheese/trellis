---
id: tlc-check-completeness-of-a-binary-tree-2-code
node: a.check-completeness-of-a-binary-tree
type: qa
step: 2
---
## Q
**LC 958 二叉树的完全性检验**｜写出 Python 实现

给二叉树根节点 `root`（节点数 `1` 到 `100`），判断它是否是完全二叉树：除最后一层外每层都满，最后一层的节点都靠左。要求 `O(n)` 时间。

## A
**思路。** 层序遍历，把空孩子也入队。用 `seen_gap` 记录是否已经出队过一个 `None`；之后再出队真实节点就返回 `False`。队列里的内容恰好是完全二叉树的「节点在前、空位在后」序列。

```python
from collections import deque

def is_complete_tree(root: TreeNode | None) -> bool:
    queue = deque([root])              # 层序遍历，连空位（None）也入队
    seen_gap = False                   # 是否已经遇到过空位
    while queue:
        node = queue.popleft()
        if node is None:
            seen_gap = True
            continue
        if seen_gap:                   # 空位之后又出现真实节点：最后一层不靠左
            return False
        queue.append(node.left)
        queue.append(node.right)
    return True
```

运行：`[1,2,3,4,5,6]` → `True`，`[1,2,3,4,5,None,7]` → `False`，`[1]` → `True`，`[1,2]` → `True`，`[1,None,2]` → `False`。

**复杂度。** 时间 `O(n)`：每个节点及其两个孩子位置各入队出队一次；空间 `O(w)`，`w` 为最大层宽，最坏 `O(n)`。

**写法要点。** `deque([root])` 让根本身为空也能直接处理；`popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`；`continue` 之后不再入队 `None` 的孩子，队列不会无限增长；不需要按层分组，一个布尔标志就够。
