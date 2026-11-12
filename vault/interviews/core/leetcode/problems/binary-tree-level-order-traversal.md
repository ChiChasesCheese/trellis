---
slug: binary-tree-level-order-traversal
---
## Q
**LC 102 二叉树的层序遍历**｜Medium

返回二叉树的层序遍历：逐层从左到右，每层一个列表。

## A
**一句话。** 队列 BFS，每轮先用 `len(queue)` 固定本层节点数，只处理这么多个。

```python
def level_order(root):
    res = []
    q = deque([root] if root else [])
    while q:
        level = []
        for _ in range(len(q)):    # 本层个数，新入队的属于下一层
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(w)`（`w` 为最宽一层）。

**易错点。**
- 内层不固定本层个数，一直弹到队空：所有节点挤进同一层，得 `[[3,9,20,15,7]]`。
- 用 `list.pop(0)` 当队列：每次 `O(n)`，整体退化成 `O(n^2)`。
- 空树返回 `[]`，不是 `[[]]`。

**追问。**
- 自底向上（LC 107）？：最后把 `res` 反转。
- 最小深度（LC 111）？：BFS 遇到的第一个叶子所在层就是答案，可提前返回。

**同模式。** LC 103 二叉树的锯齿形层序遍历、LC 199 二叉树的右视图、LC 515 在每个树行中找最大值、LC 429 N 叉树的层序遍历
