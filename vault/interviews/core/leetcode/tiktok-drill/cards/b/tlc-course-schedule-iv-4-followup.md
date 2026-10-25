---
id: tlc-course-schedule-iv-4-followup
node: b.course-schedule-iv
type: qa
step: 4
---
## Q
**LC 1462 课程表 IV**｜追问

面试官接着问：（1）不熟悉位运算，用 Floyd–Warshall 怎么写？（2）课程图里可能有环？（3）先修关系在线增加，边加边查？

## A
1. **Floyd–Warshall**：`reach[i][j]` 表示 `i` 能到达 `j`。以每个节点 `k` 作为中转，更新所有点对。

```python
def check_if_prerequisite_floyd(num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    reach = [[False] * num_courses for _ in range(num_courses)]
    for a, b in prerequisites:
        reach[a][b] = True
    for k in range(num_courses):                  # k 必须是最外层循环
        for i in range(num_courses):
            if reach[i][k]:
                for j in range(num_courses):
                    if reach[k][j]:
                        reach[i][j] = True
    return [reach[u][v] for u, v in queries]
```

   两个示例得到 `[False, True]` 和 `[True, True]`。`O(n^3)`，`n = 100` 时 `10^6` 步。中转点 `k` 必须放在最外层循环，放到里层会漏掉需要多次中转的路径。
2. **有环**：拓扑序处理不到环上的点，这些点的 `pre` 会停在不完整的值。做法：先用强连通分量（Tarjan 或 Kosaraju）缩点，同一分量内的点互相是先决条件，再在缩点后的 DAG 上做位集传播；或者直接用 Floyd–Warshall，它不依赖无环。
3. **在线加边**：新增 `a → b` 时，所有能到达 `a` 的点（包括 `a`）都能到达 `b` 以及 `b` 能到达的所有点。用 `reach` 位集：对每个 `x`，若 `x` 能到达 `a`（或就是 `a`），则 `reach[x] |= reach[b] | (1 << b)`，`O(n)` 次位运算每条边。查询仍然 `O(1)`。

**Python 提醒**：`[[False] * n] * n` 会让所有行共享同一个列表，必须写成 `[[False] * n for _ in range(n)]`；用整数当位集时，`1 << u` 只对非负 `u` 有意义，别用负下标。
