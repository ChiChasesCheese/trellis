---
slug: minimum-height-trees
---
## Q
**LC 310 最小高度树**｜Medium

树是无向图，其中任意两个顶点只通过一条路径连接。给你一棵包含 `n` 个结点（标号 `0` 到 `n - 1`）的树和 `n - 1` 条无向边 `edges`（`edges[i] = [ai, bi]`）。可以选任意结点作为根，根为 `x` 时树的高度是根到叶子的最长路径的边数；高度最小的树称为最小高度树。返回所有最小高度树的根的标号，顺序任意。`1 <= n <= 2 * 10^4`，`edges.length == n - 1`，`0 <= ai, bi < n`，`ai != bi`，所有 `(ai, bi)` 互不相同，输入保证是一棵树。例：`n = 4`, `edges = [[1,0],[1,2],[1,3]]` → `[1]`；`n = 6`, `edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]` → `[3,4]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 树的中心（center）+ 拓扑排序式的"剥叶子"（BFS 按层从外向内收缩）。

**一句话。** 反复删除当前所有叶子，直到剩下不超过 `2` 个结点，剩下的就是最小高度树的根（树的中心，至多两个）。

**识别。** 「以每个结点为根的高度」「所有最小高度的根」= 树的中心；`n = 2 * 10^4`，对每个结点都做一次 BFS 是 `O(n^2) = 4 * 10^8`，太慢，要线性。

**推导。** 以 `x` 为根的高度就是 `x` 到最远结点的距离。离所有结点都"最近"的结点在最长路径（直径）的正中间：直径有奇数个结点则中心唯一，偶数个则中心是中间两个，所以答案只有 `1` 或 `2` 个结点。从外向内一层层剥掉叶子，直径的两端最先被剥掉，最后剩下的就是中间的 `1` 或 `2` 个结点。

```python
def find_min_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    if n <= 2:  # 只有 1 个结点时没有叶子（度为 0），单独处理；2 个结点都是答案
        return list(range(n))
    adj: list[set[int]] = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    leaves = [i for i in range(n) if len(adj[i]) == 1]  # 第一层叶子
    remaining = n
    while remaining > 2:  # 剩下 1 或 2 个结点时它们就是中心
        remaining -= len(leaves)
        next_leaves: list[int] = []
        for leaf in leaves:
            (nb,) = adj[leaf]  # 叶子只有一个邻居
            adj[nb].remove(leaf)
            if len(adj[nb]) == 1:  # 邻居剥掉这个叶子后变成新的叶子
                next_leaves.append(nb)
        leaves = next_leaves
    return leaves
```

运行：示例 1 → `[1]`；示例 2 → `[3,4]`；`n = 1` → `[0]`；`n = 2` → `[0,1]`；路径 `0-1-2-3` → `[1,2]`。`n = 20000` 的链和星形都瞬间完成。

**复杂度。** 时间 `O(n)`（每个结点最多被剥一次），空间 `O(n)`。

**拓展优化。**
- 求直径再取中点，效果相同：BFS 两次，第一次从任意点找到最远点 `a`，第二次从 `a` 出发找最远点 `b` 并记录父结点，还原路径 `a..b`，中心就是路径中间的 `1` 或 `2` 个结点：

```python
from collections import deque


def find_min_height_trees_diameter(n: int, edges: list[list[int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    def farthest(src: int) -> tuple[int, list[int]]:
        parent = [-1] * n
        seen = [False] * n
        seen[src] = True
        queue = deque([src])
        last = src
        while queue:
            last = queue.popleft()  # BFS 最后出队的结点离 src 最远
            for nb in adj[last]:
                if not seen[nb]:
                    seen[nb] = True
                    parent[nb] = last
                    queue.append(nb)
        return last, parent

    a, _ = farthest(0)
    b, parent = farthest(a)
    path = [b]
    while path[-1] != a:
        path.append(parent[path[-1]])
    mid = len(path) // 2
    return path[mid - 1:mid + 1] if len(path) % 2 == 0 else [path[mid]]
```

**易错点。**
- 对每个结点做一次 BFS 求高度再取最小：正确但 `O(n^2)`，`n = 2 * 10^4` 超时。
- 把 `n = 1` 交给通用流程：没有度为 `1` 的结点，叶子列表为空，返回 `[]`，正确是 `[0]`。
- 循环条件写成 `remaining > 1`：路径 `0-1-2-3`（`n = 4`）剥完 `0`、`3` 后还会再剥一轮，把 `1`、`2` 也剥光，得不到正确的 `[1,2]`。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 1245 树的直径、LC 543 二叉树的直径。
