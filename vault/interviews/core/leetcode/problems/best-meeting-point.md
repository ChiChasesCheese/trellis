---
slug: best-meeting-point
---
## Q
**LC 296 最佳的碰头地点**｜Hard

网格里 `1` 是一个人的家。选一个格子作碰头点，使所有人到它的曼哈顿距离之和最小，返回这个最小和。

## A
**一句话。** 曼哈顿距离的行、列互不影响，各取中位数：行坐标和列坐标分别排好，取中间那个。

```python
def min_total_distance(grid):
    rows, cols = [], []
    for i, row in enumerate(grid):      # 按行扫，行坐标自然有序
        for j, v in enumerate(row):
            if v:
                rows.append(i)
    for j in range(len(grid[0])):       # 按列扫，列坐标自然有序
        for i in range(len(grid)):
            if grid[i][j]:
                cols.append(j)
    r, c = rows[len(rows) // 2], cols[len(cols) // 2]
    return (sum(abs(x - r) for x in rows)
            + sum(abs(y - c) for y in cols))
```

**复杂度。** 时间 `O(mn)`，空间 `O(人数)`。

**易错点。**
- 取平均数当碰头点：平均数不最小，中位数才最小（`[0,0,10]` 取平均点距离和 `13.3`，取中位数 `10`）。
- 把行列合在一起排序：要分开算，两个方向互相独立。
- 列坐标没排序就取中间：按行扫出来的列坐标是乱的，所以单独按列再扫一遍。

**追问。**
- 为什么中位数最优？：一维上点到 `x` 的距离和，`x` 往右挪一步，左边的点都远 1、右边都近 1，左边多就不该挪，所以停在正中。
- 碰头点必须是空地呢？：中位数落在人家里也只是一个格子，题目没禁，若禁止就在中位数附近找最近空格再比较。

**同模式。** LC 462 最少移动次数使数组元素相等 II、LC 2448 使数组相等的最小开销、LC 1703 得到连续 K 个 1 的最少相邻交换次数
