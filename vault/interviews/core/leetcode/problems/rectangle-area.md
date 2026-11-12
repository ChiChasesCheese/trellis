---
slug: rectangle-area
---
## Q
**LC 223 矩形面积**｜Medium

给两个边平行于坐标轴的矩形（左下、右上顶点），求它们覆盖的总面积。

## A
**一句话。** 容斥：两矩形面积之和减去重叠面积，重叠宽高各为 `min(右) - max(左)`，负数按 `0`。

```python
def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    w = max(0, min(ax2, bx2) - max(ax1, bx1))
    h = max(0, min(ay2, by2) - max(ay1, by1))
    return area_a + area_b - w * h
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 不相交时宽高都是负数，相乘变正：漏掉 `max(0, ·)`，`(0,0,1,1)` 与 `(2,2,3,3)` 得 `1`，应为 `2`。
- 靠「顶点是否落在对方里」判相交：十字交叉的两个矩形没有顶点在对方里，却有重叠。

**追问。**
- 怎么求交集矩形？：左下 `(max(ax1,bx1), max(ay1,by1))`，右上 `(min(ax2,bx2), min(ay2,by2))`。
- 只判断是否相交（LC 836）？：`w > 0 and h > 0`，接触不算。

**同模式。** LC 836 矩形重叠、LC 850 矩形面积 II、LC 218 天际线问题
