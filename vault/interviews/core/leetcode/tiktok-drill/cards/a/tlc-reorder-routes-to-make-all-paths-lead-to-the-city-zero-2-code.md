---
id: tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-2-code
node: a.reorder-routes-to-make-all-paths-lead-to-the-city-zero
type: qa
step: 2
---
## Q
**LC 1466 重新规划路线**｜写出 Python 实现

`n` 座城市（`2 <= n <= 5 * 10^4`）由 `n - 1` 条有向路线 `connections[i] = [a, b]` 连成一棵树（忽略方向时）。求最少反转多少条路线，才能让每座城市都能到达城市 `0`。

## A
**思路。** 建双向邻接表，`a → b` 方向记 `(b, 1)`（顺原方向、背离 `0`，需要反转），`b → a` 方向记 `(a, 0)`。从 `0` 开始用显式栈遍历，每个新节点累加进入它那条边的标记。

```python
def min_reorder(n: int, connections: list[list[int]]) -> int:
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

运行：`(6, [[0,1],[1,3],[2,3],[4,0],[4,5]])` → `3`，`(5, [[1,0],[1,2],[3,2],[3,4]])` → `2`，`(3, [[1,0],[2,0]])` → `0`；`5 × 10^4` 个节点的链 `0→1→…` 得到 `49999`，约 `6 ms`；反向链得到 `0`。

**复杂度。** 时间 `O(n)`：每条边两个邻接项，每个节点入栈一次；空间 `O(n)`。

**写法要点。** 邻接项是 `(邻居, 代价)` 元组，遍历时 `for v, cost in adj[u]` 直接解包；树上不需要记录父节点，用 `seen` 数组即可防止走回头路（树没有环，`seen` 等价于“父节点不再访问”）；`stack.pop()` 是后进先出的 DFS，换成 `deque.popleft()` 就是 BFS，结果相同；类型注释 `list[list[tuple[int, int]]]` 写在变量上，说明邻接表的形状。
