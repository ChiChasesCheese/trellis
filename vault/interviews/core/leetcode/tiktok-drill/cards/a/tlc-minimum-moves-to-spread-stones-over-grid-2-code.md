---
id: tlc-minimum-moves-to-spread-stones-over-grid-2-code
node: a.minimum-moves-to-spread-stones-over-grid
type: qa
step: 2
---
## Q
**LC 2850 将石头分散到网格图的最少移动次数**｜写出 Python 实现

`3 * 3` 的整数矩阵 `grid`（`0 <= grid[i][j] <= 9`，元素和为 `9`），每次可把一个石头移到相邻格子。返回让每个格子恰好一个石头的最少移动次数。

## A
**思路。** 把“多出来的石头”（格子里的 `k` 颗算 `k - 1` 个）列成 `extra`，空格子列成 `empty`，两者个数相等。枚举 `empty` 的所有排列，按位置与 `extra` 配对，累加曼哈顿距离，取最小。

```python
from itertools import permutations


def minimum_moves(grid: list[list[int]]) -> int:
    extra = [(r, c) for r in range(3) for c in range(3) for _ in range(grid[r][c] - 1)]   # 多出来的石头（一个格子多 k 个就重复 k-1 次）
    empty = [(r, c) for r in range(3) for c in range(3) if grid[r][c] == 0]               # 空格子
    return min(
        sum(abs(r1 - r2) + abs(c1 - c2) for (r1, c1), (r2, c2) in zip(extra, order))
        for order in permutations(empty)            # 枚举“哪颗多余石头去哪个空格”
    )
```

运行：`[[1,1,0],[1,1,1],[1,2,1]]` → `3`，`[[1,3,0],[1,0,0],[1,0,3]]` → `4`，`[[1,1,1],[1,1,1],[1,1,1]]` → `0`，`[[9,0,0],[0,0,0],[0,0,0]]` → `18`，`[[0,0,0],[0,9,0],[0,0,0]]` → `12`；`8` 个空格的最坏情形约 `15 ms`。

**复杂度。** 时间 `O(E! · E)`，`E <= 8` 是空格数，最多 `40320 × 8` 次加法；空间 `O(E)`。

**写法要点。** `for _ in range(grid[r][c] - 1)` 一行把“多 `k - 1` 颗”展开成重复的坐标，值为 `0` 的格子 `range(-1)` 是空的，不产生元素；全部格子都是 `1` 时 `empty` 为空，`permutations([])` 产生一个空元组，`sum` 得 `0`，`min` 作用在一个元素上，不需要特判；`zip(extra, order)` 把两个等长序列逐位配对，坐标元组在循环头里直接解包。
