---
id: tlc-minimum-path-sum-2-code
node: b.minimum-path-sum
type: qa
step: 2
---
## Q
**LC 64 最小路径和**｜写出 Python 实现

`m x n` 的非负整数网格 `grid`（`1 <= m, n <= 200`，元素 `0..200`）。每次只能向下或向右走一步，返回从左上角到右下角的最小路径数字和。

## A
**思路。** 一维 `dp` 表示当前行各列的最小路径和。第一行是 `grid[0]` 的前缀和。之后每行先处理第一列（只能从上来），再从左到右更新其余列：`dp[j] = min(dp[j], dp[j-1]) + row[j]`。

```python
from itertools import accumulate


def min_path_sum(grid: list[list[int]]) -> int:
    dp = list(accumulate(grid[0]))               # 第一行只能一路向右：就是前缀和
    for row in grid[1:]:
        dp[0] += row[0]                          # 第一列只能从上面来
        for j in range(1, len(row)):
            dp[j] = min(dp[j], dp[j - 1]) + row[j]   # dp[j] 还是上一行的值（从上来），dp[j-1] 已更新（从左来）
    return dp[-1]
```

**运行。** `[[1,3,1],[1,5,1],[4,2,1]]` → `7`；`[[1,2,3],[4,5,6]]` → `12`；`[[7]]` → `7`；`[[1,2,3]]` → `6`；`[[1],[2],[3]]` → `6`。

**复杂度。** 时间 `O(mn)`：每格一次 `min` 与一次加法；空间 `O(n)`，不修改输入。

**写法要点。** `accumulate(grid[0])` 一行得到首行的累计和，比手写循环短且不易错；`grid[1:]` 从第二行开始遍历；用 `dp[0] += row[0]` 单独处理第一列，使内层循环可以从 `j = 1` 开始、无需判断边界；`min(dp[j], dp[j - 1])` 依赖更新顺序（从左到右），原地覆盖时不需要再开一行。
