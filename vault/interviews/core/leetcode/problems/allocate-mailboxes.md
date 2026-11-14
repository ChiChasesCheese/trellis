---
slug: allocate-mailboxes
---
## Q
**LC 1478 安排邮筒**｜Hard

数轴上 `n` 栋房子（`n ≤ 100`），放 `k` 个邮筒，求每栋房子到最近邮筒的距离之和的最小值。

## A
**一句话。** 排序后每个邮筒管一段连续房子，放在这段中位数最省；划分型 DP：`f[b][i]` 为前 `i` 栋用 `b` 个邮筒，枚举最后一段的起点。

```python
def min_distance(houses, k):
    houses.sort()
    n = len(houses)
    # cost[i][j]：一个邮筒管 i..j 的最小距离和
    cost = [[0] * n for _ in range(n)]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            cost[i][j] = (cost[i + 1][j - 1]
                          + houses[j] - houses[i])  # 外层一对
    # f[b][i]：前 i 栋用 b 个邮筒
    f = [[inf] * (n + 1) for _ in range(k + 1)]
    f[0][0] = 0
    for b in range(1, k + 1):
        for i in range(1, n + 1):
            for j in range(b - 1, i):     # 最后一段 j..i-1
                f[b][i] = min(f[b][i],
                              f[b - 1][j] + cost[j][i - 1])
    return f[k][n]
```

**复杂度。** 时间 `O(k·n^2)`，空间 `O(k·n + n^2)`。

**易错点。**
- 忘了排序：一段「连续」房子要按坐标连续，中位数结论才成立。
- 段代价逐个加距离：`O(n)` 一次，总复杂度变 `O(k·n^3)`；用 `cost[i+1][j-1] + h[j] - h[i]` 递推。

**追问。**
- 为什么中位数最优？：邮筒往一侧挪一格，那侧更近的房子少于另一侧更远的房子，总距离不减。
- 能更快吗？：`cost` 满足四边形不等式，可用决策单调性降到 `O(k·n)` 或 wqs 二分。

**同模式。** LC 410 分割数组的最大值、LC 1335 工作计划的最低难度、LC 813 最大平均值和的分组、LC 462 最小操作次数使数组元素相等 II
