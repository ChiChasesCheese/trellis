---
slug: max-points-on-a-line
---
## Q
**LC 149 直线上最多的点数**｜Hard

平面上互不相同的点 `points`，求同一条直线上最多有多少个点。

## A
**一句话。** 枚举基点，把到其余点的方向向量用 `gcd` 约分并规范符号，哈希计数取最大再加一。

```python
def max_points(points):
    n = len(points)
    best = min(n, 2)
    for i in range(n):
        x1, y1 = points[i]
        cnt = Counter()
        for j in range(i + 1, n):
            dx = points[j][0] - x1
            dy = points[j][1] - y1
            g = math.gcd(dx, dy)     # 点不同，g > 0
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy    # 统一方向
            cnt[dx, dy] += 1
            best = max(best, cnt[dx, dy] + 1)
    return best
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 不统一方向：`(-1,-1)` 与 `(1,1)` 当成两种斜率，`[[1,1],[0,0],[2,2]]` 得 `2`，应为 `3`。
- 忘了加基点自己：`[[1,1],[2,2],[3,3]]` 得 `2`，应为 `3`。

**追问。**
- 为什么不用浮点斜率 `dy/dx`？：有精度误差，且竖线除零；约分后的整数对精确。
- 只枚举 `j > i` 为什么够？：前面的点作基点时已经统计过它们。

**同模式。** LC 447 回旋镖的数量、LC 1232 缀点成线、LC 356 直线镜像
