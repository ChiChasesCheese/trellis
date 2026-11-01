---
slug: detect-squares
---
## Q
**LC 2013 检测正方形（Detect Squares）**｜Medium

给你一个在 X-Y 平面上的点构成的数据流。设计一个算法：添加一个在数据流中的新点到某个数据结构中，可以添加重复的点，并会视作不同的点进行处理；给你一个查询点，从数据结构中选出三个点，使这三个点和查询点一同构成一个面积为正的轴对齐正方形，统计满足该要求的方案数目。轴对齐正方形的四条边长度相同，并且每条边都与 x 轴或 y 轴平行或垂直。实现 `DetectSquares` 类：`DetectSquares()` 使用空数据结构初始化；`void add(int[] point)` 向数据结构添加一个新点 `point = [x, y]`；`int count(int[] point)` 统计与点 `point` 共同构造轴对齐正方形的方案数。`point.length == 2`，`0 <= x, y <= 1000`，调用 `add` 和 `count` 的总次数最多为 `5000`。例：依次 `add([3,10])`、`add([11,2])`、`add([3,2])`、`count([11,10])`、`count([14,8])`、`add([11,2])`、`count([11,10])`，`count` 依次返回 `1, 0, 2`（重复点各算一个）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 哈希表计数 + 几何：由对角点唯一确定轴对齐正方形的另外两个顶点。

**一句话。** 用 `Counter` 记录每个点的个数；查询点 `(x, y)` 与对角点 `(px, py)`（`|px - x| == |py - y|` 且不为 0）确定正方形，另外两个顶点是 `(px, y)` 和 `(x, py)`，方案数是三个点个数的乘积。

**识别。** 「轴对齐正方形」意味着一个对角顶点和查询点就决定了全部四个顶点；「重复点算不同的点」意味着要计数、方案数相乘。调用总数 `<= 5000`，每次 `count` 遍历所有不同的点 `O(P)` 足够。

**推导。** 枚举三个点的组合 `O(P³)`，太慢。其实从查询点出发，只需枚举对角点：它必须满足 `|dx| == |dy| != 0`，另外两个顶点坐标就确定了，查表得到个数。同一个对角点出现 `c` 次、另两点各出现 `a`、`b` 次，方案数是 `c * a * b`。

```python
from collections import Counter


class DetectSquares:
    def __init__(self) -> None:
        self.pts: Counter[tuple[int, int]] = Counter()      # 点 -> 出现次数（重复点算不同的点）

    def add(self, point: list[int]) -> None:
        self.pts[(point[0], point[1])] += 1

    def count(self, point: list[int]) -> int:
        x, y = point
        ans = 0
        for (px, py), c in self.pts.items():
            # (px, py) 作为查询点的对角顶点：|dx| == |dy| 且面积为正
            if abs(px - x) == abs(py - y) and px != x:
                ans += c * self.pts[(px, y)] * self.pts[(x, py)]    # 另外两个顶点的个数相乘；Counter 缺失键返回 0 且不插入
        return ans
```

运行：示例六步 `count` 依次得到 `1, 0, 2`；只 `add([1, 1])` 后 `count([1, 1])` → `0`（对角点不能是查询点自己）。

**复杂度。** `add` 时间 `O(1)`；`count` 时间 `O(P)`，`P` 是不同点的个数；空间 `O(P)`。

**拓展优化。**
- 点很多、查询频繁：按列分组，`cols[x]` 保存该列上每个 `y` 的个数。查询点的竖线上每个点 `(x, y2)` 决定边长 `d = y2 - y`，正方形在左或右，另两个顶点 `(x ± d, y)`、`(x ± d, y2)`，每次只扫查询点所在这一列。

```python
from collections import Counter, defaultdict


class DetectSquaresByColumn:
    def __init__(self) -> None:
        self.cols: defaultdict[int, Counter[int]] = defaultdict(Counter)   # x -> {y: 个数}

    def add(self, point: list[int]) -> None:
        x, y = point
        self.cols[x][y] += 1

    def count(self, point: list[int]) -> int:
        x, y = point
        ans = 0
        for y2, c in self.cols.get(x, {}).items():       # 只看和查询点同一竖线上的点：它们决定正方形边长
            if y2 == y:
                continue
            d = y2 - y
            for x2 in (x + d, x - d):                    # 正方形在竖线左侧或右侧
                col2 = self.cols.get(x2)
                if col2:
                    ans += c * col2[y] * col2[y2]
        return ans
```

**易错点。**
- 漏掉 `px != x`：查询点自己（或和它重合的点）满足 `|dx| == |dy| == 0`，面积为 0 的退化「正方形」被计入，`add([1, 1])` 后 `count([1, 1])` 得到 `1`，正确 `0`。
- 用集合代替计数：重复点被合并，示例最后一次 `count([11, 10])` 得到 `1`，正确 `2`。
- 只考虑 `px > x`、`py > y` 的对角点：正方形可以在查询点的任意一侧，要用绝对值。

**同模式。** LC 149 直线上最多的点数、LC 447 回旋镖的数量、LC 939 最小面积矩形、LC 1 两数之和。
