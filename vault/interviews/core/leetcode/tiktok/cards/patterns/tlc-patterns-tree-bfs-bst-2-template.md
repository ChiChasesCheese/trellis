---
id: tlc-patterns-tree-bfs-bst-2-template
node: patterns.tree-bfs-bst
type: qa
step: 2
---
## Q
**二叉树 BFS 与 BST 性质｜模板：按层遍历**

写出按层处理的 BFS 模板，怎样保证一次循环恰好处理完一层？右侧视图（LC 199）和锯齿形层序（LC 103）怎样改？

## A
**按层的关键**：每一层开始时，队列里恰好是这一层的所有节点，先记下 `len(q)`，再弹出这么多个。

```python
from collections import deque
def right_side_view(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    res: list[int] = []
    q = deque([root])
    while q:
        res.append(q[-1].val)              # 这一层最右边的节点
        for _ in range(len(q)):            # 固定本层的节点数，恰好处理完一层
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return res
```

运行：`[1,2,3,null,5,null,4]` → `[1,3,4]`；`[1,2,3,4,null,null,null,5]` → `[1,3,4,5]`；`[1,null,3]` → `[1,3]`；空树 → `[]`。

**锯齿形层序（LC 103）**：同一模板，每层先按从左到右取值，再按奇偶层决定是否反转。

```python
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    res: list[list[int]] = []
    q = deque([root] if root else [])
    left_to_right = True
    while q:
        level = [node.val for node in q]
        res.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return res
print(zigzag_level_order(TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))))   # [[3], [20, 9], [15, 7]]
```

- 时间 `O(n)`，空间 `O(w)`（`w` 为最宽的一层）。
- 用 `deque`，不要用 `list.pop(0)`（`O(n)`）。
- 另一种写法：用两个列表 `cur`、`nxt` 逐层替换，不需要 `len(q)`。
