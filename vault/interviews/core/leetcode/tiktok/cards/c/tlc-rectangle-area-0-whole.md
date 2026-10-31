---
id: tlc-rectangle-area-0-whole
node: c.rectangle-area
type: qa
---
## Q
**LC 223 矩形面积**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 3 次 · 最近 2023-04-26（国内 CodeTop）

二维平面上有两个边与坐标轴平行的矩形，每个由左下顶点和右上顶点给出：第一个 `(ax1, ay1)`、`(ax2, ay2)`，第二个 `(bx1, by1)`、`(bx2, by2)`。返回两个矩形覆盖的总面积。`-10^4 <= ax1 <= ax2 <= 10^4`，`-10^4 <= ay1 <= ay2 <= 10^4`，`bx1, by1, bx2, by2` 同样范围。例：`ax1 = -3, ay1 = 0, ax2 = 3, ay2 = 4, bx1 = 0, by1 = -1, bx2 = 9, by2 = 2` → `45`；两个矩形完全重合 `(-2,-2,2,2)` 与 `(-2,-2,2,2)` → `16`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 总面积 = 两矩形面积之和 - 重叠面积；重叠宽度是 `min(右) - max(左)`，高度同理，任何一边为负就是不相交，按 `0` 算。

**识别。** 「两个轴对齐矩形的并」：容斥原理，难点只有求交集。一维区间 `[a1, a2]` 与 `[b1, b2]` 的交长度是 `max(0, min(a2, b2) - max(a1, b1))`，x 和 y 两个方向相互独立。

**推导。** 把每个单位格子标记出来再数：坐标范围 `2 * 10^4`，格子数达 `4 * 10^8`，不可行。洞察：交集仍是轴对齐矩形（或空），宽高分别由一维区间交得出，面积相乘即可。

```python
def compute_area(ax1: int, ay1: int, ax2: int, ay2: int,
                 bx1: int, by1: int, bx2: int, by2: int) -> int:
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    overlap_w = max(0, min(ax2, bx2) - max(ax1, bx1))   # x 方向交集宽度，不相交时为负，取 0
    overlap_h = max(0, min(ay2, by2) - max(ay1, by1))
    return area_a + area_b - overlap_w * overlap_h        # 容斥：重叠部分被算了两次
```

运行：示例 1 → `45`，示例 2 → `16`；不相交的 `(0,0,1,1)` 与 `(2,2,3,3)` → `2`；只在边上接触 `(0,0,1,1)` 与 `(1,0,2,1)` → `2`。

**复杂度。** 时间 `O(1)`，空间 `O(1)`。Python 整数不会溢出（其他语言面积最大约 `4 * 10^8 * 2`，仍在 32 位内，但中间量要小心）。

**拓展优化。**
- `n` 个矩形的面积并（LC 850）：坐标压缩加扫描。按 x 方向相邻的两个压缩坐标切成竖条，每条内把覆盖它的矩形的 y 区间合并求长度。

```python
from itertools import pairwise


def rectangles_union_area(rects: list[tuple[int, int, int, int]]) -> int:
    xs = sorted({x for x1, _, x2, _ in rects for x in (x1, x2)})   # 压缩后的 x 坐标
    area = 0
    for left, right in pairwise(xs):             # 每个竖条 [left, right) 内，覆盖它的矩形集合不变
        spans = sorted((y1, y2) for x1, y1, x2, y2 in rects if x1 <= left and right <= x2)
        covered = 0
        top = -10**9                             # 已合并区间的右端
        for y1, y2 in spans:
            y1 = max(y1, top)                    # 与已计入的部分重叠的那截不重复算
            if y2 > y1:
                covered += y2 - y1
                top = y2
        area += covered * (right - left)
    return area
```

此版本 `O(n² log n)`，`n` 很大时用线段树扫描线 `O(n log n)`。

**易错点。**
- 不相交时重叠宽度为负，直接相乘会得到正数（两边都负）：必须 `max(0, ...)`，不相交的 `(0,0,1,1)` 与 `(2,2,3,3)` 若漏掉会得到 `2 - 1 = 1`。
- 只判断「某个矩形的顶点在另一个里面」来算交集：十字交叉的两个矩形没有顶点落在对方里，却有重叠。
- 把重叠面积用 `abs` 而不是 `max(0, ·)`：同样错，分离的矩形会算出正的重叠。

**追问。**
- 求两个矩形的交集矩形坐标：左下 `(max(ax1, bx1), max(ay1, by1))`，右上 `(min(ax2, bx2), min(ay2, by2))`，宽高非正则无交集。
- 判断两个矩形是否相交（LC 836）：`overlap_w > 0 and overlap_h > 0`（严格大于，接触不算）。

**同模式。** LC 836 矩形重叠、LC 850 矩形面积 II、LC 335 路径交叉、LC 218 天际线问题、LC 1401 圆和矩形是否有重叠。
