---
slug: maximum-area-of-two-non-overlapping-square-submatrices
---
## Q
**LC 4016 两个不重叠子正方形的最大面积**｜Medium

`0/1` 矩阵（`m, n <= 500`），选两个边长都为 `k`、只覆盖 1、互不共享格子的正方形，求最大的单个面积 `k²`，选不出来返回 0。

## A
**一句话。** 用最大正方形 DP 求每个右下角能放的最大边长；两个 `k` 正方形不相交当且仅当右下角行差或列差 `>= k`，所以只需知道「能放 `k` 的右下角」的行、列最小最大值，从大到小找第一个满足的 `k`。

**图解。** `k = 2`：两个正方形的右下角在 `(1,1)` 和 `(2,3)`，列差 `2 >= k`，互不相交。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 178">
<rect x="26" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="56" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="12" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="26" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="56" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="26" y="80" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="56" y="80" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">深色、浅色：两个 2×2 正方形</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">右下角 (1,1)、(2,3)：列差 2 >= k</text>
<text x="16" y="160" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">答案 4</text>
</svg>

```python
def max_area(mat):
    m, n = len(mat), len(mat[0])
    K = min(m, n)
    # f[i+1][j+1]：以 (i, j) 为右下角的最大全 1 边长
    f = [[0] * (n + 1) for _ in range(m + 1)]
    box = [[inf, -inf, inf, -inf] for _ in range(K + 2)]
    for i in range(m):
        for j in range(n):
            if mat[i][j]:
                s = min(f[i][j], f[i][j + 1],
                        f[i + 1][j]) + 1
                f[i + 1][j + 1] = s
                b = box[s]   # 边长恰为 s 的右下角的行列范围
                b[0], b[1] = min(b[0], i), max(b[1], i)
                b[2], b[3] = min(b[2], j), max(b[3], j)
    for k in range(K, 0, -1):
        b, c = box[k], box[k + 1]   # 并入更大的：都能放 k
        b[0], b[1] = min(b[0], c[0]), max(b[1], c[1])
        b[2], b[3] = min(b[2], c[2]), max(b[3], c[3])
        if b[1] - b[0] >= k or b[3] - b[2] >= k:
            return k * k
    return 0
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只统计边长恰为 `k` 的右下角：能放更大正方形的位置也能放 `k`，要从大到小把范围并进来。
- 判断不相交用 `>`：右下角行差恰为 `k` 时两个正方形刚好相邻，不共享格子。

**追问。**
- 为什么只看极差？：若所有候选的行差、列差都 `< k`，任意两个都重叠；极差 `>= k` 时取那两个端点就不重叠。
- 不想推结论？：二分 `k`，检查是否有两个右下角行差或列差 `>= k`，`O(mn log)`，单调性来自大正方形里能切出小正方形。

**同模式。** LC 221 最大正方形、LC 1277 统计全为 1 的正方形子矩阵
