---
slug: largest-triangle-area
---
## Q
**LC 812 最大三角形面积**｜Easy

`points` 是平面上的点（`3 ≤ n ≤ 50`），求任意三点组成的三角形的最大面积。

## A
**一句话。** 枚举所有三点组合，用叉积（鞋带公式）算面积取最大。

```python
def largest_triangle_area(points):
    best = 0
    for a, b, c in combinations(points, 3):
        # 两向量叉积的绝对值的一半
        area = abs((b[0] - a[0]) * (c[1] - a[1])
                   - (c[0] - a[0]) * (b[1] - a[1])) / 2
        best = max(best, area)
    return best
```

**复杂度。** 时间 `O(n³)`，空间 `O(1)`。

**易错点。**
- 忘了取绝对值：叉积有正负，顺时针时面积为负，最大值就错了。
- 用海伦公式：要开方，浮点误差大，叉积全是整数更干净。

**追问。**
- `n` 很大怎么办？：最大三角形的顶点一定在凸包上，先求凸包再枚举。

**同模式。** LC 976 三角形的最大周长、LC 149 直线上最多的点数、LC 963 最小面积矩形 II
