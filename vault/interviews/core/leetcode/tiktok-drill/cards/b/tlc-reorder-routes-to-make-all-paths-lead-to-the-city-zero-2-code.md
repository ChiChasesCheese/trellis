---
id: tlc-reorder-routes-to-make-all-paths-lead-to-the-city-zero-2-code
node: b.reorder-routes-to-make-all-paths-lead-to-the-city-zero
type: qa
step: 2
---
## Q
**LC 1466 重新规划路线**｜写出 Python 实现

`n` 座城市（`2 <= n <= 5 * 10^4`）由 `n - 1` 条有向路线 `connections[i] = [a, b]` 连成一棵树（忽略方向时）。求最少反转多少条路线，才能让每座城市都能到达城市 `0`。

## A
**思路。** 建双向邻接表，`a → b` 方向记 `(b, 1)`（顺原方向、背离 `0`，需要反转），`b → a` 方向记 `(a, 0)`。从 `0` 开始递归 DFS，`dfs(u, parent)` 返回以 `u` 为根的子树里要反转的边数：对每个不是父亲的邻居 `v`，累加进入 `v` 的那条边的标记和 `v` 子树的结果。

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

运行：`(6, [[0,1],[1,3],[2,3],[4,0],[4,5]])` → `3`，`(5, [[1,0],[1,2],[3,2],[3,4]])` → `2`，`(3, [[1,0],[2,0]])` → `0`；`5 × 10^4` 个节点的链 `0→1→…` 在默认递归上限下抛 `RecursionError`，`sys.setrecursionlimit(200000)` 后得到 `49999`；反向链得到 `0`。

**复杂度。** 时间 `O(n)`：每条边两个邻接项，每个节点进入一次；空间 `O(n)`：邻接表，加上最深 `O(n)` 的递归栈（链状树会触到默认递归上限）。

**写法要点。** 邻接项是 `(邻居, 代价)` 元组，遍历时 `for v, cost in adj[u]` 直接解包；树没有环，传一个 `parent` 参数就能防止走回头路，不需要 `seen` 数组；`flips += cost + dfs(v, u)` 一行同时累加进入边的代价和子树的结果；类型注释 `list[list[tuple[int, int]]]` 写在变量上，说明邻接表的形状；嵌套函数 `dfs` 直接读外层的 `adj`。
