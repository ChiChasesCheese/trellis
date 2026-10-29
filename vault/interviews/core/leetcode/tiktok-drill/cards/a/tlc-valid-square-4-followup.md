---
id: tlc-valid-square-4-followup
node: a.valid-square
type: qa
step: 4
---
## Q
**LC 593 有效的正方形**｜追问

面试官接着问：（1）给 `n` 个点，其中有没有四个点构成正方形？（2）坐标是浮点数怎么办？（3）改成判断矩形？

## A
1. **`n` 个点里找正方形**：把点放进集合，枚举两点当作一条边，向一侧旋转 90 度得到另外两个顶点，查集合。`O(n^2)`，比枚举四元组的 `O(n^4)` 好得多。

```python
from itertools import combinations


def has_square(points: list[tuple[int, int]]) -> bool:
    pts = set(points)
    for (x1, y1), (x2, y2) in combinations(pts, 2):
        dx, dy = x2 - x1, y2 - y1
        for sx, sy in ((-dy, dx), (dy, -dx)):          # 向两侧各旋转 90 度
            if (x1 + sx, y1 + sy) in pts and (x2 + sx, y2 + sy) in pts:
                return True
    return False
```

`has_square([(0,0),(1,0),(1,1),(0,1),(5,5)])` → `True`；`has_square([(0,0),(1,0),(2,0)])` → `False`。
2. **浮点坐标**：`==` 会被舍入误差打败，改成 `math.isclose` 或乘以公倍数换成整数；整数能用就保持整数，比较才精确。
3. **矩形**：不要求等边，改查「两条对角线等长且互相平分」：枚举与 `p1` 配对的对角点，另外两点的坐标和等于 `p1` 与该点的坐标和（中点重合），并且两条对角线的平方距离相等、大于 0。

**Python 提醒**：`combinations` 按输入的顺序产出，对集合也能用，但集合迭代顺序不固定，调试时输出会变；点是列表时不能直接放进集合（列表不可哈希），要先转成元组。
