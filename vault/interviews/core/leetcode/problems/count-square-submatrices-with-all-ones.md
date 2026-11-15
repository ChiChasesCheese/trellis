---
slug: count-square-submatrices-with-all-ones
---
## Q
**LC 1277 统计全为 1 的正方形子矩阵**｜Medium

`0/1` 矩阵，数完全由 1 组成的正方形子矩阵个数。

## A
**一句话。** `f[i][j]` 是以 `(i, j)` 为右下角的最大全 1 正方形边长，等于左、上、左上三者最小值加一；它同时是以此为右下角的正方形个数，全部加起来。

**图解。** 格中是 `f` 值：右下角的 3 表示以它结尾有边长 1、2、3 的正方形各一个；全表求和 `3 + 6 + 6 = 15`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 178">
<rect x="26" y="12" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="56" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="26" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="56" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="116" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="26" y="80" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="56" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="116" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">格中是 f：以此为右下角的最大边长</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3 = min(左 2, 上 2, 左上 2) + 1</text>
<text x="16" y="160" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">每格贡献 f 个正方形，合计 15</text>
</svg>

```python
def count_squares(matrix):
    m, n = len(matrix), len(matrix[0])
    f = [[0] * (n + 1) for _ in range(m + 1)]  # 多一圈 0
    ans = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j]:
                f[i + 1][j + 1] = min(f[i][j], f[i][j + 1],
                                      f[i + 1][j]) + 1
                ans += f[i + 1][j + 1]   # 边长 1..f 各一个
    return ans
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 取三者最大值：左、上、左上任一处断了，正方形就扩不出去，必须取最小。
- 只数最大的那个正方形：边长为 `f` 意味着以此为右下角有 `f` 个正方形。

**追问。**
- 为什么是三者最小值加一？：边长 `k` 的正方形要求左、上、左上三个方向都至少有 `k-1`，反之也足够。
- 求最大正方形面积？：同一张表取最大值的平方，就是 LC 221。

**同模式。** LC 221 最大正方形、LC 1139 最大的以 1 为边界的正方形、LC 4016 两个不重叠子正方形的最大面积
