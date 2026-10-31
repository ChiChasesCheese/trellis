---
id: tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-0-whole
node: b.reorder-routes-to-make-all-paths-lead-to-the-city-zero
type: qa
---
## Q
**LC 1466 重新规划路线**｜Medium · LC TikTok 全时段热度 50/100

有 `n` 座城市，编号 `0` 到 `n - 1`，之间共有 `n - 1` 条路线，任意两座城市之间只有唯一一条路线可走（路线网是一棵树）。`connections[i] = [a, b]` 表示一条从城市 `a` 到城市 `b` 的有向路线。城市 `0` 要举办比赛，请重新规划路线方向，使每座城市都能到达城市 `0`，返回需要变更方向的**最少**路线数。数据保证重新规划后每座城市都能到达城市 `0`。`2 <= n <= 5 * 10^4`，`connections.length == n - 1`，`connections[i].length == 2`，`0 <= connections[i][0], connections[i][1] <= n - 1`，`connections[i][0] != connections[i][1]`。例：`n = 6`，`connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]` → `3`；`n = 5`，`connections = [[1,0],[1,2],[3,2],[3,4]]` → `2`；`n = 3`，`connections = [[1,0],[2,0]]` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把有向边当无向边建图，每个方向带一个标记：顺着原方向走（背离城市 `0`）标 `1`，逆着原方向走（朝向城市 `0`）标 `0`。从 `0` 出发递归遍历整棵树（不走回父亲），每走到一个新节点就累加那条边的标记；标 `1` 的边都指向远离 `0` 的方向，必须反转。`O(n)`。

**识别。** `n` 个点、`n - 1` 条边且两两唯一可达，就是树。「所有城市都能到达 `0`」等价于：以 `0` 为根，每条边都指向根（从子节点指向父节点）。一条边要不要反转，只取决于它的原方向与“靠近 `0` 的一端”是否一致，遍历一次就全知道了。

**推导。** 暴力：对每条边，去掉它后做一次遍历看 `0` 在哪一侧，`O(n^2)`。浪费：每条边哪一侧靠近 `0`，一次从 `0` 出发的遍历就能同时回答所有边。洞察：从 `0` 往外遍历，每条边第一次被走到时，先到的一端离 `0` 近（是父），后到的是子。如果原方向是「父 → 子」，就要反转，计 `1`；是「子 → 父」就不用。`n` 到 `5 × 10^4`，递归 DFS 一遍就够；一条链的深度就是 `5 × 10^4`，会超过 Python 默认递归上限，见易错点。

```python
def min_reorder(n: int, connections: list[list[int]]) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))              # 从 a 走到 b：顺着原方向，即背离城市 0，这条边要反转
        adj[b].append((a, 0))              # 从 b 走到 a：逆着原方向，即朝向城市 0，不用动

    def dfs(u: int, parent: int) -> int:   # 以 u 为根的子树里需要反转的边数
        flips = 0
        for v, cost in adj[u]:
            if v != parent:                # 树没有环：只要不走回父亲，就不会重复访问
                flips += cost + dfs(v, u)  # 进入 v 的这条边的代价 + v 子树里的代价
        return flips

    return dfs(0, -1)
```

运行：三个示例依次得到 `3`、`2`、`0`；`5 × 10^4` 个节点的链 `0→1→…`（所有边都背离 `0`）在默认递归上限下抛 `RecursionError`，`sys.setrecursionlimit(200000)` 后得到 `49999`；反向链得到 `0`。

**复杂度。** 时间 `O(n)`，每条边在邻接表里出现两次；空间 `O(n)`，其中递归栈最深 `O(n)`（链状树）。

**易错点。**
- 把图当有向图，只沿出边遍历：示例 2 得到 `0`（正确 `2`），示例 1 得到 `2`（正确 `3`），因为沿出边到不了的城市被整个漏掉。
- 两个方向的标记写反：示例 3 两条边都已经指向 `0`，标记写反会得到 `2`，正确是 `0`。
- 递归深度：链状的树深度 `5 × 10^4`，超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈 / 队列（见追问）。
- 递归里忘了排除父亲（不传 `parent`）：邻接表是双向的，`u` 会走回刚来的父亲，无限递归。

**追问。**
- 输出具体要反转的边：遍历到 `cost == 1` 时记下 `(u, v)`。
- 树很深、不想递归：显式栈，用 `seen` 数组防止走回头路，每个新节点累加进入它那条边的标记：
```python
def min_reorder_stack(n: int, connections: list[list[int]]) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))              # 从 a 走到 b：顺着原方向，即背离城市 0，这条边要反转
        adj[b].append((a, 0))              # 从 b 走到 a：逆着原方向，即朝向城市 0，不用动
    seen = [False] * n
    seen[0] = True
    stack = [0]
    flips = 0
    while stack:
        u = stack.pop()
        for v, cost in adj[u]:
            if not seen[v]:
                seen[v] = True
                flips += cost
                stack.append(v)
    return flips
```
- 反过来要求城市 `0` 能到达所有城市：标记取反，答案是 `(n - 1) - 原答案`，因为每条边要么朝向 `0` 要么背离 `0`。
- 一般有向图中，从 `s` 到 `t` 至少要反转几条边：沿原方向的边代价 `0`，逆向的代价 `1`，用双端队列做 `0-1 BFS`。

**同模式。** LC 1971 寻找图中是否存在路径、LC 310 最小高度树、LC 1376 通知所有员工所需的时间、LC 834 树中距离之和。
