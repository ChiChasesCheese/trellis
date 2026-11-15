---
slug: cherry-pickup-ii
---
## Q
**LC 1463 摘樱桃 II**｜Hard

`grid[r][c]` 是樱桃数。两个机器人分别从左上角 `(0,0)` 和右上角 `(0,n-1)` 出发，每步下移一行，列可 `-1`、`0`、`+1`（不出界），到最后一行结束。路过的格子樱桃被摘光，两人同格只算一次。求最多摘到多少樱桃。

## A
**一句话。** 两个机器人同步一行一行下移，状态是（行，机器人 A 的列，机器人 B 的列）；每格从上一行 9 种列组合里取最大。

```python
def cherry_pickup(grid):
    m, n = len(grid), len(grid[0])
    def val(r, a, b):                 # 同格只算一次
        return grid[r][a] + (grid[r][b] if a != b else 0)
    # f[r][a][b]：两人到第 r 行、分别在 a 列和 b 列的最大樱桃数
    f = [[[-inf] * n for _ in range(n)] for _ in range(m)]
    f[0][0][n - 1] = val(0, 0, n - 1)
    for r in range(1, m):
        for a in range(n):
            for b in range(n):
                prev = max(f[r - 1][x][y]
                           for x in (a - 1, a, a + 1)
                           for y in (b - 1, b, b + 1)
                           if 0 <= x < n and 0 <= y < n)
                f[r][a][b] = prev + val(r, a, b)
    return max(map(max, f[-1]))
```

**复杂度。** 时间 `O(m · n² · 9)`，空间 `O(m · n²)`。

**易错点。**
- 两人分别做一遍摘樱桃：路径重叠的格子会被重复计数，两人必须同时规划。
- 同格重复计分：`a == b` 时只加一次。
- 初始状态没设：只有 `f[0][0][n-1]` 有值，其余为 `-inf`，否则会出现不存在的起点。

**追问。**
- 为什么两人同步下移？：这样状态只需一个行号，列只会同行相遇，不会错开。
- 和 LC 741 摘樱桃有何不同？：那题一个人往返，可转化为两人同时走，但可以右、下混走；这里每步固定下移一行。

**同模式。** LC 741 摘樱桃、LC 931 下降路径最小和、LC 64 最小路径和
