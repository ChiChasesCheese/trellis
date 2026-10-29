---
id: tlc-number-of-submatrices-that-sum-to-target-2-code
node: a.number-of-submatrices-that-sum-to-target
type: qa
step: 2
---
## Q
**LC 1074 元素和为目标值的子矩阵数量**｜写出 Python 实现

整数矩阵 `matrix`（行列数各 `1` 到 `100`，元素在 `-1000` 到 `1000`）和整数 `target`（`-10^8` 到 `10^8`）。返回元素和等于 `target` 的非空子矩阵数量。要求时间 `O(R^2 · C)`。

## A
**思路。** 外两层循环枚举上下边界，内部维护列和数组 `col`；对 `col` 用「前缀和 + `Counter`」数和为 `target` 的子数组：扫描时先查 `s - target` 出现过几次，再把当前前缀和记入。

```python
from collections import Counter


def num_submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    m, n = len(matrix), len(matrix[0])
    ans = 0
    for top in range(m):
        col = [0] * n                      # col[c]：第 top..bottom 行、第 c 列的和
        for bottom in range(top, m):
            col = [a + b for a, b in zip(col, matrix[bottom])]
            seen = Counter({0: 1})         # 前缀和 -> 出现次数；空前缀和为 0
            s = 0
            for v in col:                  # 把 col 当一维数组：数和为 target 的子数组
                s += v
                ans += seen[s - target]    # 以当前列结尾、前缀和为 s - target 的起点个数
                seen[s] += 1
    return ans
```

运行：`[[0,1,0],[1,1,1],[0,1,0]]`、`target = 0` → `4`；`[[1,-1],[-1,1]]`、`target = 0` → `5`；`[[904]]`、`target = 0` → `0`；`[[5]]`、`target = 5` → `1`。

**复杂度。** 时间 `O(R^2 · C)`：`R(R+1)/2` 个行对，每对 `O(C)`；空间 `O(C)`。

**写法要点。** `Counter({0: 1})` 一步建出带空前缀的计数表；`Counter` 对缺失键读出 `0` 且**不会插入**，所以 `seen[s - target]` 可以放心查询（`defaultdict(int)` 会在读取时插入键，污染表）；先查询再更新，保证不把当前位置自己算进去；`zip` 加列表推导生成新的 `col`，不修改 `matrix`。
