---
slug: detect-squares
---
## Q
**LC 2013 检测正方形（Detect Squares）**｜Medium

数据流不断 `add` 平面点（可重复，算不同的点）；`count(point)` 统计有多少种选三个已加入的点，与查询点构成面积为正的轴对齐正方形。

## A
**一句话。** `Counter` 记每个点的个数，枚举对角点 `(px, py)`（`|dx| == |dy|` 且不为 0），另两个顶点个数相乘。

```python
class DetectSquares:
    def __init__(self):
        self.pts = Counter()          # 点 -> 个数

    def add(self, point):
        self.pts[tuple(point)] += 1

    def count(self, point):
        x, y = point
        ans = 0
        for (px, py), c in self.pts.items():
            if abs(px - x) == abs(py - y) and px != x:
                ans += c * self.pts[(px, y)] \
                         * self.pts[(x, py)]
        return ans
```

**复杂度。** `add` 为 `O(1)`，`count` 为 `O(P)`（`P` 为不同点数），空间 `O(P)`。

**易错点。**
- 漏掉 `px != x`：与查询点重合的点满足 `|dx| == |dy| == 0`，`add([1,1])` 后 `count([1,1])` 得 `1`，应为 `0`。
- 用集合代替计数：重复点被合并，少算方案。
- 只看 `px > x`、`py > y`：正方形可在查询点任意一侧，要用绝对值。

**追问。**
- 点很多时怎么加速？：按 x 分组存 y 的计数，只枚举同列的点，边长由此确定，`count` 为 `O(同列点数)`。

**同模式。** LC 149 直线上最多的点数、LC 447 回旋镖的数量、LC 939 最小面积矩形、LC 1 两数之和
