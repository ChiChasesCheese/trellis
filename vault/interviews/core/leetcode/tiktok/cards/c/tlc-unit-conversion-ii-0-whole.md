---
id: tlc-unit-conversion-ii-0-whole
node: c.unit-conversion-ii
type: qa
---
## Q
**LC 3535 单位转换 II**｜Medium · LC TikTok 全时段热度 26/100

有 `n` 种单位，编号 `0..n - 1`。给定长度为 `n - 1` 的 `conversions`，`conversions[i] = [source, target, factor]` 表示 `1` 个 `source` 单位等于 `factor` 个 `target` 单位。再给 `queries`，`queries[i] = [unitA, unitB]`。对每个查询，返回 `1` 个 `unitA` 等于多少个 `unitB`，这个数写成最简分数 `p/q`，返回 `p * q^(-1) mod (10^9 + 7)`（`q^(-1)` 是 `q` 的模逆元）。`2 <= n <= 10^5`，`1 <= factor <= 10^9`，`1 <= queries.length <= 10^5`，保证单位 `0` 可以通过正向或反向转换的组合唯一地转换为任何其他单位（即这些转换构成一棵树）。例：`conversions = [[0,1,2],[0,2,6]]`，`queries = [[1,2],[1,0]]` → `[3, 500000004]`（`1` 个单位 1 等于 3 个单位 2，等于 1/2 个单位 0）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 从单位 `0` 出发在树上 DFS，算出「1 个单位 0 等于多少个单位 `v`」的值 `ratio[v]` 及其模逆元；任意查询 `A -> B` 的答案是 `ratio[B] / ratio[A]`。

**识别。** 「n 个节点、n - 1 条带比例的边，回答任意两点的比值」：边构成一棵树，比值沿路径连乘，只需要以一个点为基准做一次遍历，不需要每次查询重新找路径。除法在模 `10^9 + 7` 下用模逆元。

**推导。** 每次查询 DFS 找路径连乘，`O(n · q)`。洞察：路径 `A → B` 的乘积等于 `0 → B` 的乘积除以 `0 → A` 的乘积（公共部分抵消）。所以预处理 `ratio[v] = 1 个单位 0 等于多少个 v`，沿边 `s -> t` 乘以 `factor`，沿反向边乘以 `factor` 的逆元。再预处理 `inv_ratio[v] = ratio[v]` 的逆元（边上同样用逆元的逆元即 `factor`），查询时只做一次乘法，不用每次求逆。

```python
MOD = 10**9 + 7


def unit_conversion(conversions: list[list[int]], queries: list[list[int]]) -> list[int]:
    n = len(conversions) + 1
    graph: list[list[tuple[int, int, int]]] = [[] for _ in range(n)]   # (邻居, 乘数, 乘数的逆元)
    for source, target, factor in conversions:
        inv = pow(factor, -1, MOD)               # factor < MOD 且 MOD 是质数，逆元存在
        graph[source].append((target, factor, inv))   # 1 个 source = factor 个 target
        graph[target].append((source, inv, factor))   # 反向：1 个 target = 1/factor 个 source

    ratio = [0] * n                              # ratio[v]：1 个单位 0 等于多少个单位 v
    inv_ratio = [0] * n                          # ratio[v] 的模逆元
    ratio[0] = inv_ratio[0] = 1

    def dfs(u: int, parent: int) -> None:
        for v, mul, inv in graph[u]:
            if v != parent:
                ratio[v] = ratio[u] * mul % MOD
                inv_ratio[v] = inv_ratio[u] * inv % MOD
                dfs(v, u)

    dfs(0, -1)
    # 1 个 A = 1/ratio[A] 个单位 0 = ratio[B]/ratio[A] 个 B
    return [ratio[b] * inv_ratio[a] % MOD for a, b in queries]
```

运行：示例 1 `[[1,2],[1,0]]` → `[3, 500000004]`；示例 2（`conversions = [[0,1,2],[0,2,6],[0,3,8],[2,4,2],[2,5,4],[3,6,3]]`，`queries = [[1,2],[0,4],[6,5],[4,6],[6,1]]`）→ `[3,12,1,2,83333334]`。

**复杂度。** 时间 `O(n + q)`（预处理的逆元用 `pow` 共 `n - 1` 次，每次 `O(log MOD)`），空间 `O(n)`。

**拓展优化。**
- 链状树 `n = 10^5` 时递归深度超限，改成 BFS（见追问）。
- 不需要预存逆元数组：查询时 `ratio[b] * pow(ratio[a], -1, MOD)`，每次多一个 `O(log MOD)`，`q = 10^5` 时也能过，代码更短。

**易错点。**
- 把答案当整数除法：结果是分数，只能在模意义下用逆元，`1 / 2` 对应 `500000004`。
- 反向边忘了取逆元：`1 个 target = 1/factor 个 source`，乘 `factor` 就是反的。
- 最坏深度：链状树 `n = 10^5`，CPython 默认递归上限约 1000，会抛 `RecursionError`，要 `sys.setrecursionlimit` 调高或改用 BFS。

**追问。**
- 递归深度超限：用 BFS（每个节点出队时更新邻居），逻辑一致。

```python
from collections import deque

MOD = 10**9 + 7


def unit_conversion_bfs(conversions: list[list[int]], queries: list[list[int]]) -> list[int]:
    n = len(conversions) + 1
    graph: list[list[tuple[int, int, int]]] = [[] for _ in range(n)]
    for source, target, factor in conversions:
        inv = pow(factor, -1, MOD)
        graph[source].append((target, factor, inv))
        graph[target].append((source, inv, factor))
    ratio = [0] * n
    inv_ratio = [0] * n
    ratio[0] = inv_ratio[0] = 1
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    while queue:                                 # 从单位 0 开始层层推进，每个节点只更新一次
        u = queue.popleft()
        for v, mul, inv in graph[u]:
            if not seen[v]:
                seen[v] = True
                ratio[v] = ratio[u] * mul % MOD
                inv_ratio[v] = inv_ratio[u] * inv % MOD
                queue.append(v)
    return [ratio[b] * inv_ratio[a] % MOD for a, b in queries]
```

- 图里允许出现环或多余的边（LC 399 除法求值）：同样的 DFS / BFS，遇到已访问的点时可顺便校验比值是否一致。

**同模式。** LC 399 除法求值、LC 990 等式方程的可满足性、LC 1257 最小公共区域、LC 2316 统计无向图中无法互相到达点对数、LC 1319 连通网络的操作次数。
