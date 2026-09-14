---
id: leetcode-q-dungeon-game-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787102261582
tags: [lc::174, leetcode, pattern, recall]
---
## Q
网格图 DP 中，若某格的状态依赖其“到达终点还需要多少资源”（如最小血量），且约束是必须保持中间某个量非负，应该如何设计 dfs 方向和状态定义？

## A
从终点往起点反向定义 dfs(i,j) = 从 (i,j) 出发到达终点所需的最小初始值（如最小血量）。递推时先算出到达下一格所需值，减去当前格的收益/伤害，再与 0 取 max（保证血量不会为负）：need = max(0, dfs(next) - d[i][j])，最终答案为 dfs(0,0) + 1。这是因为“正向累加和”无法唯一确定最优路径（路径上血量正负交替时，走法会影响能否存活），必须反向定义“需求量”才能让子问题独立、可用 DP/记忆化求解。

**Evidence**

```
@cache
def dfs(i: int, j: int) -> int:
    if i == m - 1 and j == n - 1:
        return max(0, -d[i][j])
    need = math.inf
    for ni, nj in ((i + 1, j), (i, j + 1)):
        if not (0 <= ni < m and 0 <= nj < n):
            continue
        need = min(need, max(0, dfs(ni, nj) - d[i][j]))
    return need
return dfs(0, 0) + 1
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F174%20-%20Dungeon%20Game)
