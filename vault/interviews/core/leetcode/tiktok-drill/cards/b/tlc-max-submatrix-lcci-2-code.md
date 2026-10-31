---
id: tlc-max-submatrix-lcci-2-code
node: b.max-submatrix-lcci
type: qa
step: 2
---
## Q
**面试题 17.24 最大子矩阵**｜写出 Python 实现

`N × M` 整数矩阵（`1 <= N, M <= 200`，元素可正可负可为 `0`）。返回元素总和最大的子矩阵 `[r1, c1, r2, c2]`（左上角、右下角的行列号），有多个时返回任意一个。

## A
**思路。** 外层枚举上边界 `top`，内层枚举下边界 `bottom`，同时维护 `col`（这几行按列求和）。对 `col` 做 Kadane：`cur` 是以当前列结尾的最大子段和，`cur` 不为正就丢掉重新从当前列开始，同时记起点；每次刷新全局最大值时记下 `[top, start, bottom, c]`。

```python
def get_max_matrix(matrix: list[list[int]]) -> list[int]:
    rows, cols = len(matrix), len(matrix[0])
    best = float("-inf")
    ans = [0, 0, 0, 0]
    for top in range(rows):
        col = [0] * cols                   # col[c]：第 top..bottom 行、第 c 列的和
        for bottom in range(top, rows):
            col = [a + b for a, b in zip(col, matrix[bottom])]
            cur, start = 0, 0              # 对 col 做 Kadane：最大子段和，同时记起点
            for c, v in enumerate(col):
                if cur > 0:
                    cur += v
                else:
                    cur, start = v, c      # 前面的和不为正：丢掉，从 c 重新开始
                if cur > best:
                    best = cur
                    ans = [top, start, bottom, c]
    return ans
```

运行：`[[-1,0],[0,-1]]` → `[0,1,0,1]`；`[[-5]]` → `[0,0,0,0]`；`[[1,-2,3],[-4,5,-6],[7,-8,9]]` → `[2,2,2,2]`；`[[-3,-1],[-2,-4]]` → `[0,1,0,1]`。

**复杂度。** 时间 `O(R^2 · C)`：`(top, bottom)` 共 `R(R+1)/2` 对，每对做 `O(C)` 的累加和 Kadane；空间 `O(C)`。

**写法要点。** `[a + b for a, b in zip(col, matrix[bottom])]` 用 `zip` 做逐列相加并生成新列表，不会改动 `matrix` 的行；`best = float("-inf")` 保证全负矩阵也能取到最大的单个元素；Kadane 写成「`cur > 0` 就延续，否则重启」，一个分支同时处理了起点更新。
