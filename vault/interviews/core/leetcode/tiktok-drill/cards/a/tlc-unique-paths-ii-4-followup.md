---
id: tlc-unique-paths-ii-4-followup
node: a.unique-paths-ii
type: qa
step: 4
---
## Q
**LC 63 不同路径 II**｜追问

面试官接着问：（1）除了数量，再返回**一条**可行路径？（2）如果没有障碍，能不能不用 DP？（3）如果机器人可以上下左右四个方向走（不能重复经过同一格），DP 还成立吗？

## A
1. **返回一条路径**：先照常填完 `dp`，再从终点倒推，哪个来源格的 `dp` 非零就说明能从那边来。

```python
def one_path(obstacle_grid: list[list[int]]) -> str:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    dp[0][1] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if obstacle_grid[i - 1][j - 1] == 0:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    if dp[m][n] == 0:
        return ""
    i, j, moves = m, n, []
    while (i, j) != (1, 1):                  # 从终点倒着走：哪个来源格有路径，就是上一步
        if dp[i - 1][j]:
            moves.append("D")
            i -= 1
        else:
            moves.append("R")
            j -= 1
    return "".join(reversed(moves))
```

运行：样例 1 → `"RRDD"`，`[[0,1],[0,0]]` → `"DR"`，`[[0,1],[1,0]]` → `""`。

2. **无障碍**：路径就是 `m+n-2` 步里选 `m-1` 步向下，`math.comb(m + n - 2, m - 1)`，`O(min(m, n))`；`3 x 3` → `6`。
3. **四个方向**：图里有环，不再是 DAG，「最后一步来自哪」的分解失效；数简单路径在一般图上是 `#P` 完全问题，没有已知的多项式算法，只能回溯（LC 980 不同路径 III 就是 `m*n <= 20` 的回溯）。若只问最短路径条数，则用 BFS 分层累加。

另外，空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：Python 整数不溢出，无障碍的 `100 x 100` 网格会算出约 `2.3 * 10^58` 的大数；换成 Java / C++ 要注意题目给的 `2 * 10^9` 上界只对测试数据成立。
