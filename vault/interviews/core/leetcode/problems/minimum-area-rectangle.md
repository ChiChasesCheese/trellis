---
slug: minimum-area-rectangle
---
## Q
**LC 939 最小面积矩形**｜Medium

平面上互不相同的点，求由这些点作顶点、边平行于坐标轴的矩形的最小面积，没有则返回 `0`。

## A
**一句话。** 点放进哈希集合，枚举每对点当对角线，另外两个角由它们唯一确定，查表即可。

```python
def min_area_rect(points):
    pts = [tuple(p) for p in points]   # 列表不可哈希
    seen = set(pts)
    areas = (
        abs(x1 - x2) * abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(pts, 2)
        if x1 != x2 and y1 != y2       # 排除共线
        and (x1, y2) in seen and (x2, y1) in seen
    )
    return min(areas, default=0)
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 漏写 `x1 != x2 and y1 != y2`：共线两点的另两角就是它们自己，被当成面积 `0` 的矩形，示例 1 得 `0`，应为 `4`。
- 直接 `set(points)`：元素是列表，抛 `TypeError`。
- 没有矩形时 `min` 作用于空序列抛 `ValueError`，要 `default=0`。

**追问。**
- 点数到 `10^5` 怎么办？：按列扫描，同列每对 `(y1,y2)` 记录上次出现的列 `x`，再遇到同一对就成矩形。
- 边不必平行于坐标轴（LC 963）？：中点相同、长度相同的两条线段构成矩形，按（中点，长度）分组，仍是 `O(n²)`。

**同模式。** LC 963 最小面积矩形 II、LC 750 角矩形的数量、LC 593 有效的正方形、LC 149 直线上最多的点数
