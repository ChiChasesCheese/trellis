---
id: tlc-diagonal-traverse-2-code
node: a.diagonal-traverse
type: qa
step: 2
---
## Q
**LC 498 对角线遍历**｜写出 Python 实现

矩阵 `mat` 大小 `m x n`，`1 <= m, n <= 10^4` 且 `1 <= m * n <= 10^4`，元素在 `[-10^5, 10^5]`。从左上角出发先向右上、再向左下交替，按对角线遍历顺序返回所有元素。

## A
**思路。** 行优先扫描，把元素按 `i + j` 分组追加到 `defaultdict(list)` 中；每组内行号递增（从右上到左下）。依次处理 `d = 0 … m + n - 2`：`d` 为奇数时原样输出（向左下），偶数时反向输出（向右上）。

```python
from collections import defaultdict

def find_diagonal_order(mat: list[list[int]]) -> list[int]:
    m, n = len(mat), len(mat[0])
    diagonals: defaultdict[int, list[int]] = defaultdict(list)
    for i, row in enumerate(mat):
        for j, v in enumerate(row):
            diagonals[i + j].append(v)             # 同一条反对角线上 i + j 相同；行优先扫描时 i 递增
    result: list[int] = []
    for d in range(m + n - 1):
        line = diagonals[d]                        # 此时 line 是从右上到左下
        result.extend(line if d % 2 else reversed(line))   # d 为偶数时向右上走，要从左下到右上
    return result
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,4,7,5,3,6,8,9]`，`[[1,2],[3,4]]` → `[1,2,3,4]`，`[[7]]` → `[7]`，`[[1,2,3]]` → `[1,2,3]`，`[[1],[2],[3]]` → `[1,2,3]`；`1 x 10000` 和 `10000 x 1` 都返回长度 `10000`。

**复杂度。** 时间 `O(m·n)`；空间 `O(m·n)`，分组存放所有元素。

**写法要点。** `defaultdict(list)` 省去"键不存在就先创建"的判断；`enumerate(mat)` 与 `enumerate(row)` 同时拿到下标和值；`line if d % 2 else reversed(line)` 是条件表达式，`extend` 既接受列表也接受 `reversed` 迭代器，不必先复制；`range(m + n - 1)` 恰好覆盖所有对角线，空的组不会出现（每个 `d` 至少含一个元素）。
