---
slug: right-triangles
---
## Q
**LC 3128 直角三角形**｜Medium

二维 0/1 矩阵 `grid`。选三个值为 `1` 的格子，若其中一个与另一个同行、同时与第三个同列，则三者构成直角三角形。求直角三角形的数目。

## A
**一句话。** 以直角顶点为枚举对象：对每个值为 `1` 的格子，同行的其他 `1` 的个数乘同列的其他 `1` 的个数。

```python
def number_of_right_triangles(grid):
    rows = [sum(r) for r in grid]
    cols = [sum(c) for c in zip(*grid)]
    return sum((rows[i] - 1) * (cols[j] - 1)
               for i, r in enumerate(grid)
               for j, v in enumerate(r) if v)
```

**复杂度。** 时间 `O(mn)`，空间 `O(m + n)`。

**易错点。**
- 没减去自己：行里的 `1` 包含直角顶点本身，要 `- 1`。
- 重复计数：每个三角形有唯一的直角顶点，所以按顶点计一次不会重复。

**追问。**
- 换成"任意三点能构成三角形"？：需要统计不共线的组合，难度大幅上升。

**同模式。** LC 1267 统计参与通信的服务器、LC 1582 二进制矩阵中的特殊位置、LC 2482 行和列中一和零的差值
