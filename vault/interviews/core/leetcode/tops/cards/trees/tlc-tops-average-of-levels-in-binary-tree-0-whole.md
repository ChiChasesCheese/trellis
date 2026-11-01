---
id: tlc-tops-average-of-levels-in-binary-tree-0-whole
node: trees.average-of-levels-in-binary-tree
type: qa
---
## Q
**LC 637 二叉树的层平均值（Average of Levels in Binary Tree）**｜Easy · 全公司热度第 1078 名 · Top Interview 150

给定一个非空二叉树的根节点 `root`，以数组的形式返回每一层节点的平均值。与实际答案相差 `10^-5` 以内的答案可以被接受。树中节点数量在 `[1, 10^4]` 范围内，`-2^31 <= Node.val <= 2^31 - 1`。例：`root = [3,9,20,null,null,15,7]` → `[3.0, 14.5, 11.0]`；`root = [3,9,20,15,7]` → `[3.0, 14.5, 11.0]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 层序遍历（BFS）：队列中按层处理，每层求和再除以节点数。

**一句话。** 用队列做 BFS，每次开始处理一层前记下队列长度 `size`，恰好弹出 `size` 个节点求和，平均值 = 和 / `size`。

**识别。** 「每一层」的统计量（平均值、最大值、右视图）都是层序遍历的固定模板：一层一层处理，处理前固定本层节点数。

**推导。** 先把每层节点收集成二维列表再求平均，要多存一份节点；其实每层只需要「和」与「个数」。BFS 里本层开始时队列里恰好是这一层的所有节点，所以固定 `size`，边弹边累加，同时把孩子入队作为下一层。

```python
from collections import deque


def average_of_levels(root: TreeNode) -> list[float]:
    ans: list[float] = []
    queue = deque([root])
    while queue:
        size = len(queue)                 # 此刻队列里恰好是同一层的全部节点
        total = 0
        for _ in range(size):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        ans.append(total / size)
    return ans
```

运行：`[3,9,20,null,null,15,7]` → `[3.0, 14.5, 11.0]`，`[3,9,20,15,7]` → `[3.0, 14.5, 11.0]`，`[-2147483648, 2147483647]`（根加一个孩子）→ `[-2147483648.0, 2147483647.0]`，单节点 `[5]` → `[5.0]`。

**复杂度。** 时间 `O(n)`，空间 `O(w)`，`w` 是最宽一层的节点数（最坏 `O(n)`）。

**拓展优化。**
- 深度优先：用 `sums[d]`、`counts[d]` 按深度累计，遍历完再逐层相除；不需要队列，递归深度等于树高。

```python
def average_of_levels_dfs(root: TreeNode | None) -> list[float]:
    sums: list[int] = []                  # sums[d]、counts[d]：第 d 层的节点值之和、节点数
    counts: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(sums):
            sums.append(0)
            counts.append(0)
        sums[depth] += node.val
        counts[depth] += 1
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [s / c for s, c in zip(sums, counts)]
```

**易错点。**
- 在循环里用 `range(len(queue))` 之外的方式反复读取 `len(queue)`（比如 `while len(queue) > 0` 里边弹边入队）：队列长度在变，会把相邻两层混在一起。必须在处理前把 `size` 存下来。
- 用整数除法 `//`：`[3,9,20,15,7]` 得到 `[3, 14, 11]`，正确 `[3.0, 14.5, 11.0]`。
- C++/Java 里节点值是 32 位整数，一层的和会超过 `int`：累加要用 `long`/`double`；Python 整数不会溢出。

**同模式。** LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 103 二叉树的锯齿形层序遍历、LC 515 在每个树行中找最大值。
