---
id: tlc-minimum-depth-of-binary-tree-4-followup
node: b.minimum-depth-of-binary-tree
type: qa
step: 4
---
## Q
**LC 111 二叉树的最小深度**｜追问

面试官接着问：（1）除了深度，再返回从根到最近叶子的那条路径？（2）不用 BFS，写一个正确的递归版本，它在什么输入下有问题？（3）树非常宽（比如完全二叉树），BFS 的内存是多少，DFS 呢？

## A
1. **返回路径**：BFS 时记录每个节点的父节点，找到第一个叶子后沿父指针回到根，再反转。

```python
from collections import deque


def nearest_leaf_path(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.left is None and node.right is None:
            path: list[int] = []
            cur: TreeNode | None = node
            while cur is not None:                # 沿父指针回到根
                path.append(cur.val)
                cur = parent[cur]
            return path[::-1]
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                queue.append(child)
    return []
```

运行：`[3,9,20,null,null,15,7]` → `[3, 9]`，`[2,null,3,null,4,null,5,null,6]` → `[2, 3, 4, 5, 6]`。

2. **递归版**：`if root is None: return 0`；左空则 `return 1 + f(root.right)`，右空则 `return 1 + f(root.left)`；都在才 `1 + min(...)`。逻辑正确，但在 `10^5` 个节点的链上触发 `RecursionError`；要么 BFS，要么用显式栈模拟。
3. **内存**：BFS 的队列至多容纳相邻两层，完全二叉树的最底层约 `n/2` 个节点，空间 `O(n)`；DFS 的栈是树高，完全二叉树只有 `O(log n)`。所以「宽而浅」的树 DFS 省内存，「窄而深」的树 BFS 省内存，而且 BFS 能提前结束。

**Python 提醒**：`TreeNode` 没有定义 `__eq__` 时按对象身份哈希，可以直接当 `dict` 的键；如果自定义了 `__eq__` 却没定义 `__hash__`，实例就变得不可哈希。
