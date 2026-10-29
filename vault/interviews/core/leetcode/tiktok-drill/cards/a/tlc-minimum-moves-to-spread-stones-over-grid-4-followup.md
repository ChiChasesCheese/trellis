---
id: tlc-minimum-moves-to-spread-stones-over-grid-4-followup
node: a.minimum-moves-to-spread-stones-over-grid
type: qa
step: 4
---
## Q
**LC 2850 将石头分散到网格图的最少移动次数**｜追问

面试官接着问：（1）网格变成 `n × n`，排列枚举不行了？（2）要输出具体的移动序列？（3）每个格子的目标石头数不再是 `1`？

## A
1. **更大的网格**：排列是 `E!`，`E` 到 `15` 就不行了。用状压 DP：`dp[mask]` 表示前 `popcount(mask)` 颗多余石头已经落在 `mask` 标出的空格里时的最小代价，转移是让下一颗多余石头选一个还没用的空格，`O(2^E · E)`。

```python
from math import inf


def minimum_moves_dp(grid: list[list[int]]) -> int:
    extra = [(r, c) for r in range(3) for c in range(3) for _ in range(grid[r][c] - 1)]
    empty = [(r, c) for r in range(3) for c in range(3) if grid[r][c] == 0]
    m = len(empty)
    dp = [inf] * (1 << m)
    dp[0] = 0
    for mask in range(1 << m):
        i = mask.bit_count()               # 已经安置了前 i 颗多余石头
        if i == m:
            continue
        for j in range(m):
            if not mask >> j & 1:
                cost = abs(extra[i][0] - empty[j][0]) + abs(extra[i][1] - empty[j][1])
                nxt = mask | 1 << j
                dp[nxt] = min(dp[nxt], dp[mask] + cost)
    return dp[-1]
```

   对 `3 × 3` 的全部 `24310` 种石头分布，这个 DP 与排列枚举的结果完全一致；示例 1、2 得到 `3`、`4`。再大就用匈牙利算法（`O(E^3)`，Python 里可以用 `scipy.optimize.linear_sum_assignment`）或最小费用流。
2. **输出移动序列**：对每个匹配好的（石头，空格）对，先沿行再沿列逐格移动，每步是 `(from, to)`。不同石头的路径可能交叉，但每一步只需要“源格子里至少有一颗石头”，按匹配顺序依次执行总是合法的。
3. **目标量不为 `1`**：供给是“多出目标的部分”，需求是“缺少的部分”，两侧数量不再一一对应单个格子，变成运输问题，用最小费用最大流：源点连供给格子（容量=多余数），需求格子连汇点（容量=缺少数），网格相邻格子之间连容量无穷、费用 `1` 的边。

**Python 提醒**：`int.bit_count()` 要 Python 3.10 以上，旧版本用 `bin(mask).count("1")`；`mask >> j & 1` 的运算优先级是先移位再按位与，不需要括号；`itertools.permutations` 返回的元组里元素是同一批对象，枚举时没有拷贝成本，但结果顺序按输入位置而不是按值，重复元素也会重复出现（这里坐标互不相同，不受影响）。
