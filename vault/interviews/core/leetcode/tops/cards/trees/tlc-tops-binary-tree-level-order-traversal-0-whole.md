---
id: tlc-tops-binary-tree-level-order-traversal-0-whole
node: trees.binary-tree-level-order-traversal
type: qa
---
## Q
**LC 102 二叉树的层序遍历**｜Medium · 全公司热度第 246 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你二叉树的根节点 `root`，返回其节点值的层序遍历（即逐层地，从左到右访问所有节点）。树中节点数目在范围 `[0, 2000]` 内，`-1000 <= Node.val <= 1000`。

例：`root = [3,9,20,null,null,15,7]` → `[[3],[9,20],[15,7]]`；`root = [1]` → `[[1]]`；`root = []` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 广度优先搜索（BFS）按层分批：每轮用当前队列长度切出一整层。

**一句话。** 用队列做 BFS，每一轮先记下队列里现有的结点数（正好是这一层的结点数），弹出这么多个，同时把它们的孩子入队。

**识别。** 「逐层」「每层单独一个列表」是 BFS 的信号，且需要知道层的边界。同类题：右视图、每层最大值、锯齿形遍历、最小深度。`n <= 2000`，线性。

**推导。** 只用队列做 BFS 可以得到按层顺序的扁平序列，但分不出层的边界。关键观察是：开始处理一层时，队列里恰好装着这一层的全部结点，且还没有下一层的结点；所以此刻的 `len(q)` 就是本层结点数，弹出这么多个，后面入队的就自然是下一层。

```python
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    res: list[list[int]] = []
    q = deque([root] if root else [])       # 空树时队列为空，直接返回 []
    while q:
        level = []
        for _ in range(len(q)):             # 先固定本层结点数，循环中入队的孩子属于下一层
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

**运行。** `[3,9,20,null,null,15,7]` → `[[3], [9, 20], [15, 7]]`；`[1]` → `[[1]]`；`[]` → `[]`；`[1,2,null,3]` → `[[1], [2], [3]]`。

**复杂度。** 时间 `O(n)`，空间 `O(w)`，`w` 是最宽一层的结点数（最坏 `O(n)`）。

**拓展优化。**
- DFS 写法：带深度参数递归，第一次到达某一深度时新开一个列表，先左后右保证层内从左到右。
```python
def level_order_dfs(root: TreeNode | None) -> list[list[int]]:
    res: list[list[int]] = []
    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(res):               # 第一次到达这一层
            res.append([])
        res[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return res
```
- 从下往上（LC 107）：结果 `res[::-1]`；锯齿形（LC 103）：奇数层 `level.reverse()`。

**易错点。**
- 循环里用 `while q` 而不固定本层数量：边弹边入队，层的边界消失，例 1 得到扁平的 `[3, 9, 20, 15, 7]`。
- 空树时直接 `deque([root])`：队列里放进 `None`，弹出后读 `.val` 抛 `AttributeError`。
- 用 `list.pop(0)` 当队列：每次 `O(n)`，整体退化成 `O(n²)`；要用 `deque`。

**同模式。** LC 199 二叉树的右视图、LC 1161 最大层内元素和、LC 103 锯齿形层序遍历、LC 111 二叉树的最小深度。
