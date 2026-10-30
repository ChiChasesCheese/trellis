---
id: tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-4-followup
node: b.reorder-routes-to-make-all-paths-lead-to-the-city-zero
type: qa
step: 4
---
## Q
**LC 1466 重新规划路线**｜追问

面试官接着问：（1）要输出具体是哪几条路线需要反转？（2）反过来要求城市 `0` 能到达所有城市，答案怎么变？（3）图不是树，是一般有向图，求从 `s` 到 `t` 至少反转几条边？

## A
1. **输出具体路线**：遍历时记下 `cost == 1` 的那条边。邻接项里多存一个原始边，或者直接把 `(u, v)` 收集起来。

```python
def reorder_edges(n: int, connections: list[list[int]]) -> list[list[int]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))
        adj[b].append((a, 0))
    seen = [False] * n
    seen[0] = True
    stack = [0]
    flipped: list[list[int]] = []
    while stack:
        u = stack.pop()
        for v, cost in adj[u]:
            if not seen[v]:
                seen[v] = True
                if cost:
                    flipped.append([u, v])         # 原方向 u -> v 背离 0，需要反转
                stack.append(v)
    return flipped
```

   示例 2 返回 `[[1, 2], [3, 4]]` 的某个排列（顺序取决于遍历顺序），共 `2` 条。
2. **`0` 到达所有城市**：此时每条边都应该是「父 → 子」，标记取反。每条边要么朝向 `0` 要么背离 `0`，所以答案是 `(n - 1) - 原答案`。示例 1：`5 - 3 = 2`。
3. **一般有向图的最少反转路径**：沿原方向走一条边代价 `0`，逆着走（相当于反转它）代价 `1`，问题变成最短路。边权只有 `0` 和 `1`，用双端队列做 `0-1 BFS`：代价 `0` 的邻居 `appendleft`，代价 `1` 的邻居 `append`，`O(V + E)`。

**Python 提醒**：`collections.deque` 两端 `O(1)`，是 `0-1 BFS` 的标准工具；`list.pop(0)` 是 `O(n)`。递归遍历树时，`sys.setrecursionlimit` 只能提高 Python 层的限制，深度到 `5 × 10^4` 仍可能耗尽 C 栈，竞赛与面试里更稳的做法是显式栈。
