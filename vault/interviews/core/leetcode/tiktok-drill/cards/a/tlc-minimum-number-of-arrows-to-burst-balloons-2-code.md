---
id: tlc-minimum-number-of-arrows-to-burst-balloons-2-code
node: a.minimum-number-of-arrows-to-burst-balloons
type: qa
step: 2
---
## Q
**LC 452 用最少数量的箭引爆气球**｜写出 Python 实现

`points[i] = [xstart, xend]` 是第 `i` 个气球的水平直径（`1 <= len(points) <= 10^5`，`-2^31 <= xstart < xend <= 2^31 - 1`）。一支箭在坐标 `x` 射出，引爆所有满足 `xstart <= x <= xend` 的气球。返回引爆全部气球所需的最少箭数。

## A
**思路。** 按右端点升序排序。维护上一支箭的位置 `last`；遍历每个气球，若它的左端点大于 `last`，说明上一支箭够不着，新射一支并把 `last` 设为它的右端点（射得越靠右，能顺带射爆的后续气球越多）。

```python
from math import inf
from operator import itemgetter


def find_min_arrow_shots(points: list[list[int]]) -> int:
    arrows = 0
    last = -inf                            # 上一支箭的位置
    for start, end in sorted(points, key=itemgetter(1)):   # 按右端点排序
        if start > last:                   # 上一支箭够不着：新射一支，射在 end（尽量靠右）
            arrows += 1
            last = end
    return arrows
```

运行：`[[10,16],[2,8],[1,6],[7,12]]` → `2`，`[[1,2],[3,4],[5,6],[7,8]]` → `4`，`[[1,2],[2,3],[3,4],[4,5]]` → `2`，`[[-2147483648,2147483647]]` → `1`，`[[1,10],[2,3],[4,5]]` → `2`。

**复杂度。** 时间 `O(n log n)`：排序；扫描 `O(n)`。空间 `O(n)`：`sorted` 生成新列表。

**写法要点。** `key=itemgetter(1)` 比 `lambda p: p[1]` 更快更简洁；循环变量直接解包成 `start, end`；初始值用 `-inf`，保证第一个气球一定触发新箭，不用单独特判「是否为空」，也不用担心坐标可能小到 `-2^31`；用 `sorted` 不修改调用者的列表，要省空间可以改成 `points.sort(key=itemgetter(1))`。
