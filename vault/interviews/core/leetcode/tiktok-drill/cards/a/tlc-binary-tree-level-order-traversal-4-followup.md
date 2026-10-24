---
id: tlc-binary-tree-level-order-traversal-4-followup
node: a.binary-tree-level-order-traversal
type: qa
step: 4
---
## Q
**LC 102 二叉树的层序遍历**｜追问

面试官接着问：（1）求二叉树的**最小深度**，怎样利用 BFS 提前返回？（2）改成 **N 叉树**的层序遍历？（3）树非常宽、内存吃紧，哪里会占空间，能怎么省？

## A
1. **最小深度（LC 111）**：BFS 按层推进，第一个出队的叶子（左右孩子都为空）所在的层就是最小深度。在层循环外维护 `depth += 1`，遇到叶子立即 `return depth`，不必遍历完整棵树；DFS 则必须走完所有分支。
2. **N 叉树（LC 429）**：节点有 `children` 列表，把两个 `if` 换成 `queue.extend(node.children)`，其余完全不变。
3. **内存**：队列最多同时装下相邻两层的节点，峰值约为最宽一层的宽度 `w`，完全二叉树约 `n/2`。如果只要每层的聚合（和、最大值、个数），在层循环里边弹边累加，不必存 `level` 列表；输出本身要 `O(n)` 就无法省。

```python
def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue, depth = deque([root]), 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if not node.left and not node.right:
                return depth
            queue.extend(c for c in (node.left, node.right) if c)
    return depth
```

**Python 提醒**：`deque` 不支持切片，`queue[1:3]` 会报 `TypeError`；要看队首用 `queue[0]`。遍历 `deque` 的同时往里 `append` 会抛 `RuntimeError: deque mutated during iteration`，所以才用 `range(len(queue))` 的快照而不是 `for node in queue`。
