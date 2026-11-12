---
slug: minimum-edge-reversals-so-every-node-is-reachable
---
## Q
**LC 2858 可以到达每一个节点的最少边反转次数（Minimum Edge Reversals So Every Node Is Reachable）**｜Hard

给你一个 `n` 个点的简单有向图（没有重复边），节点编号为 `0` 到 `n - 1`。如果这些边是双向边，那么这个图形成一棵树。给你整数 `n` 和二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示从 `ui` 到 `vi` 有一条有向边。边反转指的是把一条边的方向反转。对每个节点 `i`，分别独立计算：从节点 `i` 出发经过一系列有向边可以到达所有节点，最少需要多少次边反转。返回长度为 `n` 的数组 `answer`，`answer[i]` 是从节点 `i` 出发到达所有节点的最少边反转次数。`2 <= n <= 10^5`，`edges.length == n - 1`，`edges[i].length == 2`，`0 <= ui == edges[i][0] < n`，`0 <= vi == edges[i][1] < n`，`ui != vi`，输入保证如果边是双向边，可以得到一棵树。例：`n = 4`，`edges = [[2,0],[2,1],[1,3]]` → `[1,1,0,2]`；`n = 3`，`edges = [[1,2],[2,0]]` → `[2,0,1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 换根 DP（rerooting）：先算以 0 为根的答案，再沿树边 `O(1)` 地把答案推到每个邻居。

**一句话。** 无向视角下它是一棵树，从根出发每条边「朝外」才能走通；以 0 为根时数出需要反转的边数，换根时只有被换的那条边的朝向要求改变，所以 `ans[v] = ans[u] ± 1`。

**识别。** 「树上对每个节点分别求一个值，相邻节点的答案只差一条边」是换根 DP 的典型特征。`n = 10^5`，对每个根重做一次 DFS 是 `O(n²)`，需要 `O(n)`。

**推导。** 树的边集固定。以 `r` 为根时，每条边必须从父指向子才能走通：原方向就是父到子的边不用反转，反过来的要反转，所以答案 = 「原方向与『朝外』相反的边数」。建图时给每条边同时挂两个方向：`u -> v` 权重 0（顺着走，不用反转），`v -> u` 权重 1（逆着走，要反转）。先 DFS 求 `ans[0]` = 沿树向外走的权重和。根从 `u` 换到相邻的 `v`，只有边 `(u, v)` 的要求变了：原来 `u -> v` 顺着走（权重 0）时，`v` 作根要走 `v -> u` 方向，这条边需要反转，所以 `+1`；原来权重是 1 的则 `-1`，其余的边相对根的朝向不变。

```python
from collections import defaultdict


def min_edge_reversals(n: int, edges: list[list[int]]) -> list[int]:
    graph: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v in edges:
        # 沿原方向 u -> v 走：不用反转
        graph[u].append((v, 0))
        # 逆着走 v -> u：这条边必须反转
        graph[v].append((u, 1))
    ans = [0] * n

    # 以 0 为根时，所有边都朝外所需的反转数
    def count_from_root(u: int, parent: int) -> int:
        total = 0
        for v, w in graph[u]:
            if v != parent:
                total += w + count_from_root(v, u)
        return total

    def reroot(u: int, parent: int) -> None:
        for v, w in graph[u]:
            if v != parent:
                # 根从 u 换到 v：边 (u, v) 的朝向要求翻转
                # 原来不用反转（w = 0）现在要反转 +1
                # 原来要反转（w = 1）现在不用 -1
                ans[v] = ans[u] + (1 if w == 0 else -1)
                reroot(v, u)

    ans[0] = count_from_root(0, -1)
    reroot(0, -1)
    return ans
```

运行：`(4, [[2,0],[2,1],[1,3]])` → `[1, 1, 0, 2]`，`(3, [[1,2],[2,0]])` → `[2, 0, 1]`，`(2, [[0,1]])` → `[0, 1]`，`(2, [[1,0]])` → `[1, 0]`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 递归深度：树退化成长度 `10^5` 的链时递归深度到 `10^5`，需要提高递归上限或者改成迭代。用 BFS 按层记下 `(父, 子, 权重)`，第一遍累加 `ans[0]`，第二遍按同样顺序推答案；父节点一定排在子节点前面。

```python
from collections import deque


def min_edge_reversals_bfs(n: int, edges: list[list[int]]) -> list[int]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append((v, 0))
        graph[v].append((u, 1))
    ans = [0] * n
    # 按 BFS 顺序记下 (父, 子, 边权)，父一定出现在子之前
    order: list[tuple[int, int, int]] = []
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v, w in graph[u]:
            if not seen[v]:
                seen[v] = True
                # 累计根为 0 时的反转数
                ans[0] += w
                order.append((u, v, w))
                queue.append(v)
    for u, v, w in order:
        ans[v] = ans[u] + (1 if w == 0 else -1)
    return ans
```

**易错点。**
- 换根时符号写反：`+1` 和 `-1` 交换，示例一得到 `[1, 1, 2, 0]`，正确 `[1, 1, 0, 2]`。
- 对每个节点各做一次 DFS：`O(n²)`，`n = 10^5` 超时。
- 最坏深度：`edges = [[0,1],[1,2],...]` 的链有 `10^5` 层，CPython 默认递归上限约 `1000`，上面的递归版会抛 `RecursionError`，需要 `sys.setrecursionlimit` 调高或改用上面的 BFS 版。

**追问。**
- 为什么换根只差 `±1`？边 `(u, v)` 把树分成两侧，`u` 一侧的边相对根的朝向不变，`v` 一侧也不变；只有这条边自己的朝向要求从「`u` 到 `v`」变成「`v` 到 `u`」，所以差恰好 `1`。
- 图里有环（不再是树）怎么办？要变成最小代价可达性问题：先缩点（SCC），再在 DAG 上算最小树形图（Chu-Liu/Edmonds），已经是另一道题；本题的树性质是 `O(n)` 的前提。
- 要同时输出每个根下该反转哪些边？再记一个集合：根为 `0` 时收集权重为 `1` 的边，换根时该边加入或移出集合；输出规模最坏 `O(n^2)`，通常只回答某一个根。

**同模式。** LC 834 树中距离之和、LC 1466 重新规划路线、LC 310 最小高度树、LC 543 二叉树的直径。
