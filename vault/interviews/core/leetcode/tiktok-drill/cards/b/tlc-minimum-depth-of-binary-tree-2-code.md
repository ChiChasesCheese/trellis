---
id: tlc-minimum-depth-of-binary-tree-2-code
node: b.minimum-depth-of-binary-tree
type: qa
step: 2
---
## Q
**LC 111 二叉树的最小深度**｜写出 Python 实现

二叉树（节点数 `0` 到 `10^5`，值在 `[-1000, 1000]`）从根到最近叶子的路径上有几个节点？叶子是没有孩子的节点；空树返回 `0`。

## A
**思路。** BFS：队列里放 `(节点, 深度)`，按入队顺序弹出，深度单调不减；第一个弹出的叶子就是最浅的，直接返回它的深度。

```python
from collections import deque


def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue = deque([(root, 1)])                    # (节点, 它的深度)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                          # BFS 按层推进：第一个叶子就是最浅的
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0
```

运行：`[3,9,20,null,null,15,7]` → `2`，`[2,null,3,null,4,null,5,null,6]` → `5`，`[]` → `0`，`[1,2]` → `2`，`10^5` 个节点的链 → `100000`。

**复杂度。** 时间 `O(n)`，最浅叶子出现时提前结束；空间 `O(w)`，`w` 为最大层宽。

**写法要点。** `deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`，BFS 一律用 `deque`；把深度和节点打包成元组入队，省掉按层计数的外层循环；末尾的 `return 0` 不会执行到（非空树一定有叶子），只为让函数每条路径都有返回值。
