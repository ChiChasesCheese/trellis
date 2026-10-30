---
id: tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-4-followup
node: b.reorder-routes-to-make-all-paths-lead-to-the-city-zero
type: qa
step: 4
---
## Q
**LC 1466 重新规划路线**｜追问

面试官接着问：（1）要输出具体是哪几条路线需要反转？（2）反过来要求城市 `0` 能到达所有城市，答案怎么变？（3）图不是树，是一般有向图，求从 `s` 到 `t` 至少反转几条边？（4）`5 × 10^4` 个城市连成一条链，递归爆栈怎么办？

## A
1. **输出具体路线**：遍历时记下 `cost == 1` 的那条边。邻接项里多存一个原始边，或者直接把 `(u, v)` 收集起来。

```python
def reorder_edges(n: int, connections: list[list[int]]) -> list[list[int]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))
        adj[b].append((a, 0))
    flipped: list[list[int]] = []

    def dfs(u: int, parent: int) -> None:
        for v, cost in adj[u]:
            if v != parent:
                if cost:
                    flipped.append([u, v])         # 原方向 u -> v 背离 0，需要反转
                dfs(v, u)

    dfs(0, -1)
    return flipped
```

   示例 2 返回 `[[1, 2], [3, 4]]`，共 `2` 条。
2. **`0` 到达所有城市**：此时每条边都应该是「父 → 子」，标记取反。每条边要么朝向 `0` 要么背离 `0`，所以答案是 `(n - 1) - 原答案`。示例 1：`5 - 3 = 2`。
3. **一般有向图的最少反转路径**：沿原方向走一条边代价 `0`，逆着走（相当于反转它）代价 `1`，问题变成最短路。边权只有 `0` 和 `1`，用双端队列做 `0-1 BFS`：代价 `0` 的邻居 `appendleft`，代价 `1` 的邻居 `append`，`O(V + E)`。
4. **深链爆栈**：链状的树深度 `5 × 10^4`，递归抛 `RecursionError`。可以 `sys.setrecursionlimit(200000)`，或改成显式栈，用 `seen` 数组防止走回头路，每个新节点累加进入它那条边的标记：

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

   `5 × 10^4` 个节点的链 → `49999`，不受递归上限影响。

**Python 提醒**：`collections.deque` 两端 `O(1)`，是 `0-1 BFS` 的标准工具；`list.pop(0)` 是 `O(n)`。递归遍历树时，`sys.setrecursionlimit` 调高后，CPython 3.12 以后的纯 Python 递归不再占 C 栈，`5 × 10^4` 层可以跑通；更老的版本仍可能耗尽 C 栈，所以面试里要说明深度问题并给出显式栈。
