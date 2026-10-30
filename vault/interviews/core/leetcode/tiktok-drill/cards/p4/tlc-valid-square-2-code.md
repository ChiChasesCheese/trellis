---
id: tlc-valid-square-2-code
node: p4.valid-square
type: qa
step: 2
---
## Q
**LC 593 有效的正方形**｜写出 Python 实现

四个点 `p1`、`p2`、`p3`、`p4`，每个是 `[x, y]`，顺序任意，`-10^4 <= xi, yi <= 10^4`。返回它们能否构成正方形。

## A
**思路。** 算 6 个两两平方距离并排序。排序后前四个是边，后两个是对角线：边必须相等且大于 0，对角线必须相等且等于边的平方的 2 倍。这个判据与点的输入顺序无关。

```python
from itertools import combinations


def valid_square(p1: list[int], p2: list[int], p3: list[int], p4: list[int]) -> bool:
    def dist2(a: list[int], b: list[int]) -> int:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2   # 平方距离，全程整数

    d = sorted(dist2(a, b) for a, b in combinations((p1, p2, p3, p4), 2))   # 6 条两两距离
    # 四条边相等且 > 0（排除重合点），两条对角线相等且恰为边平方的 2 倍
    return d[0] > 0 and d[0] == d[3] and d[4] == d[5] == 2 * d[0]
```

运行：`[0,0],[1,1],[1,0],[0,1]` → `True`；`[0,0],[1,1],[1,0],[0,12]` → `False`；`[1,0],[-1,0],[0,1],[0,-1]` → `True`；四个 `[0,0]` → `False`；四点共线 `[0,0],[1,0],[2,0],[3,0]` → `False`。

**复杂度。** 时间 `O(1)`：固定 6 个距离，排序 6 个数；空间 `O(1)`。

**写法要点。** `combinations(points, 2)` 恰好生成 6 个无序点对，比手写双重循环不易漏；用生成器直接喂给 `sorted`，不建中间列表；链式比较 `d[4] == d[5] == 2 * d[0]` 一行表达「两条对角线相等且是边的 2 倍」；平方距离保持整数，所以所有比较都是精确的。
