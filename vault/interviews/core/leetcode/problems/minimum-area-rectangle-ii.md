---
slug: minimum-area-rectangle-ii
---
## Q
**LC 963 最小面积矩形 II**｜Medium

给平面上互不相同的点，可以组成边不必平行于坐标轴的矩形。返回由这些点中四个点组成的矩形的最小面积，没有则返回 `0`。

## A
**一句话。** 矩形的两条对角线中点相同、长度相等；把所有点对按「中点和对角线长度」分组，同组内任取两对点就是一个矩形，面积由叉积给出。

```python
def min_area_free_rect(points):
    groups = defaultdict(list)
    for p, q in combinations(points, 2):
        key = (p[0] + q[0], p[1] + q[1],     # 中点（乘 2）
               (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
        groups[key].append((p, q))
    best = inf
    for pairs in groups.values():
        for (p1, p2), (p3, p4) in combinations(pairs, 2):
            # p1 p3 p2 p4 是矩形，面积 = 两条邻边的叉积
            area = abs((p3[0] - p1[0]) * (p4[1] - p1[1])
                       - (p4[0] - p1[0]) * (p3[1] - p1[1]))
            best = min(best, area)
    return best if best < inf else 0
```

**复杂度。** 时间 `O(n^2)`（最坏同组点对很多时更高），空间 `O(n^2)`。

**易错点。**
- 只比较中点：中点相同的两条线段若长度不同，是菱形或一般平行四边形。
- 面积用边长乘积开方：用叉积的绝对值，全程整数。
- 找不到矩形直接返回 `inf`：题目要求返回 `0`。

**追问。**
- 为什么叉积就是面积？：以 `p1` 为公共顶点，`p1p3` 与 `p1p4` 是矩形相邻两边，叉积的模等于它们围成平行四边形的面积，这里就是矩形。
- 另一条思路？：枚举三个点，检查直角并推出第四个点是否存在，复杂度 `O(n^3)`。

**同模式。** LC 939 最小面积矩形、LC 593 有效的正方形、LC 149 直线上最多的点数、LC 1232 缀点成线
