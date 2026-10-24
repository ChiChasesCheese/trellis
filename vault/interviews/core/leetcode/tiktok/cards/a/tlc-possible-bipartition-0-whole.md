---
id: tlc-possible-bipartition-0-whole
node: a.possible-bipartition
type: qa
---
## Q
**LC 886 可能的二分法**｜Medium · TikTok 高频

把编号 `1..n` 的 `n` 个人分进任意大小的两组。给定整数 `n` 和数组 `dislikes`，`dislikes[i] = [ai, bi]` 表示不允许把 `ai` 和 `bi` 分到同一组。当可以用这种方法把所有人分成两组时返回 `true`，否则返回 `false`。`1 <= n <= 2000`，`0 <= dislikes.length <= 10^4`，`dislikes[i].length == 2`，`1 <= dislikes[i][j] <= n`，`ai < bi`，`dislikes` 中每一组都不同。例：`n = 4, dislikes = [[1,2],[1,3],[2,4]]` → `true`（`[1,4]` 与 `[2,3]`）；`n = 3, dislikes = [[1,2],[1,3],[2,3]]` → `false`；`n = 5, dislikes = [[1,2],[2,3],[3,4],[4,5],[1,5]]` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把「互相讨厌」建成无向图，问题就是判断图是否为**二分图**（bipartite graph）：用 BFS 给每个连通块染色（相邻点必须异色），遇到相邻点同色就返回 `False`；每个连通块都要查。`O(n + m)`。

**识别。** 「分成两组，某些对不能同组」= 二着色（two-coloring）。等价说法：图里没有长度为奇数的环。`n <= 2000`、边至多 `10^4`，`O(n + m)` 很轻。**图可能不连通**，不能只从 `1` 号开始染。

**推导。** 暴力：枚举 `2^n` 种分组，检查每条边 → 浪费：一旦确定了一个人的组，他所有的「敌人」必须在另一组，选择被强制传播 → 选一个起点任意染色，BFS 逐个把邻居染成相反色；碰到已染色且与自己同色的邻居，说明存在奇数环，直接失败；每个连通块的起点颜色任选，互不影响。

```python
from collections import deque

def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    color = [0] * (n + 1)                          # 0 = 未分组，1 / -1 = 两个组
    for start in range(1, n + 1):                  # 图可能不连通：每个连通块都要查
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:           # 互相讨厌的人落在同一组
                    return False
                if color[v] == 0:
                    color[v] = -color[u]           # 敌人的敌人放另一组
                    queue.append(v)
    return True
```

运行：`(4, [[1,2],[1,3],[2,4]])` → `True`，`(3, [[1,2],[1,3],[2,3]])` → `False`，`(5, [[1,2],[2,3],[3,4],[4,5],[1,5]])` → `False`，`(1, [])` → `True`；`n = 2000` 的一条链 → `True`。

**复杂度。** 时间 `O(n + m)`：每个点入队一次，每条边检查两次；空间 `O(n + m)`：邻接表与颜色数组。

**易错点。**
- 必须对每个连通块起一次 BFS：`n = 6`、`dislikes = [[1,2],[3,4],[4,5],[3,5]]` 里 `{3,4,5}` 是一个三角形（奇数环），只从 `1` 出发会得到 `True`，正确是 `False`。
- 颜色用 `1 / -1` 取反：`color[v] = -color[u]`；若用 `0 / 1` 就不能用 `0` 表示「未染色」。
- 判断冲突要看「已染色的邻居」：只在未染色时染色而不检查已染色的邻居，会漏掉奇数环。

**追问。**
- 并查集（Union-Find）做法：对每个人，所有敌人必须同组，把他们合并；若某条边的两端落在同一集合就失败。适合边是在线到来的场景。
- 递归 DFS 着色：`n = 2000` 的链会触发 `RecursionError`（默认深度 1000），所以这里用 BFS 或显式栈。
- 要输出一种合法分组：把颜色为 `1` 的编号和颜色为 `-1` 的编号分别收集。

**同模式。** LC 785 判断二分图、LC 1042 不邻接植花、LC 802 找到最终的安全状态、LC 261 以图判树。
