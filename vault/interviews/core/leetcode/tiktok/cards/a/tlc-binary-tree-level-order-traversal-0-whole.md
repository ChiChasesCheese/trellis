---
id: tlc-binary-tree-level-order-traversal-0-whole
node: a.binary-tree-level-order-traversal
type: qa
---
## Q
**LC 102 二叉树的层序遍历**｜Medium · 近一年被问：美国 0 次、国内 10 次 · CodeTop 国内累计 88 次 · 最近 2026-10（面试记录）

给二叉树的根节点 `root`，返回其节点值的**层序遍历**：逐层地，从左到右访问所有节点，每层一个列表。树中节点数在 `[0, 2000]` 内，`-1000 <= Node.val <= 1000`。例：`root = [3,9,20,null,null,15,7]` → `[[3],[9,20],[15,7]]`；`root = [1]` → `[[1]]`；`root = []` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用队列（`deque`）做广度优先搜索（BFS）；每轮循环开头用 `len(queue)` 记下「这一层有几个节点」，恰好处理这么多个，处理时新入队的孩子自然属于下一层。`O(n)`。

**识别。** 「逐层」「每层一个列表」「离根最近的先访问」都指向 BFS：队列先进先出，节点按到根的距离从近到远出队。难点只有一个：怎么知道层的边界。

**推导。** 暴力：DFS 带上深度 `d`，把值放进 `res[d]` → 也是 `O(n)`，但单链树深度 2000 会超过 Python 默认递归上限 1000。BFS 的三种划分层的办法：队列里存 `(node, depth)`，每个元素多带一个数；用「当前层 / 下一层」两个列表；每轮开头拍下 `len(queue)` 的快照。快照最省：不带额外数据，也不用换列表。入队前队列里恰好只有第 `d` 层的节点，所以快照就是这层的宽度。

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

**复杂度。** 时间 `O(n)`：每个节点入队、出队各一次；空间 `O(w)`，`w` 是最宽一层的节点数（完全二叉树约 `n/2`）。

**易错点。**
- 内层不拍快照，写成 `while queue:` 一直弹到空：所有节点挤进同一层，示例一得到 `[[3, 9, 20, 15, 7]]`。
- 用 `list.pop(0)` 当队列：每次 `O(n)`，整体退化成 `O(n^2)`；要用 `deque.popleft()`。
- 空树返回 `[]`，别返回 `[[]]`。

**追问。**
- 自底向上（LC 107）：最后 `res.reverse()`。
- 最小深度（LC 111）：BFS 遇到的第一个叶子，它所在的层号就是答案，可以提前返回。
- N 叉树的层序（LC 429）：把两个 `if` 换成 `queue.extend(node.children)`。

**同模式。** LC 103 锯齿形层序遍历、LC 107 层序遍历 II、LC 199 二叉树的右视图、LC 515 每行最大值、LC 111 二叉树的最小深度、LC 429 N 叉树的层序遍历。
