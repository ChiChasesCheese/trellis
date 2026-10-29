---
id: tlc-minimum-area-rectangle-2-code
node: a.minimum-area-rectangle
type: qa
step: 2
---
## Q
**LC 939 最小面积矩形**｜写出 Python 实现

`points` 是平面上互不相同的点（`1 <= points.length <= 500`，`0 <= xi, yi <= 4 * 10^4`）。返回以这些点为顶点、边与坐标轴平行的矩形的最小面积，没有就返回 `0`。

## A
**思路。** 点放进集合。用 `combinations(pts, 2)` 枚举所有点对作对角线，要求 `x`、`y` 都不同，再查另外两个角是否在集合里，在就产出面积。最后对产出的面积取最小，没有产出就返回 `0`。

```python
from itertools import combinations


def min_area_rect(points: list[list[int]]) -> int:
    pts = [tuple(p) for p in points]       # 列表不可哈希，转成元组
    seen = set(pts)
    areas = (
        abs(x1 - x2) * abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(pts, 2)
        if x1 != x2 and y1 != y2 and (x1, y2) in seen and (x2, y1) in seen   # 另外两个角也在
    )
    return min(areas, default=0)           # 没有矩形时返回 0
```

运行：`[[1,1],[1,3],[3,1],[3,3],[2,2]]` → `4`，`[[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]` → `2`，`[[0,0]]` → `0`，`[[0,0],[1,1]]` → `0`；`500` 个随机点约 `4 ms`。

**复杂度。** 时间 `O(n^2)`：约 `n(n-1)/2 ≈ 12.5` 万对，每对常数次集合查找；空间 `O(n)`。

**写法要点。** `combinations(pts, 2)` 生成无序点对，不用手写双重 `for` 和下标；`for (x1, y1), (x2, y2) in …` 在循环头里直接解包；生成器表达式配 `min(…, default=0)`，既不建中间列表，也不用先判空；`tuple(p)` 转换一次，后面都用元组做集合成员检查；`and` 的短路顺序让便宜的不等判断在前、集合查找在后。
