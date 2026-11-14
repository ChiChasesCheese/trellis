---
slug: search-a-2d-matrix
---
## Q
**LC 74 搜索二维矩阵**｜Medium

矩阵每行递增，且每行首元素大于上一行末元素，判断 `target` 是否存在，要求 `O(log(mn))`。

## A
**一句话。** 按行拼起来就是一个升序数组：在虚拟下标 `[0, mn)` 上二分，用 `divmod` 换算行列。

**图解。** 把矩阵按行拼成一维，虚拟下标用 `divmod(mid, n)` 换回行列。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 160">
<rect x="30" y="16" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="66" y="16" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="102" y="16" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="138" y="16" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="156.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="30" y="52" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48.0" y="74.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="66" y="52" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84.0" y="74.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="102" y="52" width="36" height="36" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="74.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">16</text>
<rect x="138" y="52" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="156.0" y="74.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="30" y="88" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48.0" y="110.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">23</text>
<rect x="66" y="88" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84.0" y="110.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="102" y="88" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="110.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">34</text>
<rect x="138" y="88" width="36" height="36" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="156.0" y="110.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<text x="33" y="26" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="69" y="26" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="105" y="26" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="141" y="26" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="33" y="62" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="69" y="62" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="105" y="62" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="141" y="62" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="33" y="98" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="69" y="98" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<text x="105" y="98" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="141" y="98" text-anchor="start" font-size="8" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<text x="184" y="34" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小字：虚拟下标</text>
<text x="184" y="52" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n = 4 列</text>
<text x="30" y="140" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">mid = 6 → divmod(6, 4) = (1, 2) → 16</text>
</svg>

```python
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, n)    # 除数是列数 n
        if matrix[r][c] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < m * n and matrix[lo // n][lo % n] == target
```

**复杂度。** 时间 `O(log(mn))`，空间 `O(1)`。

**易错点。**
- 换算用了行数 `m`：`2x4` 矩阵里 `mid=4` 得行号 `2`，`IndexError`；除数应是列数 `n`。
- 结束后不检查 `lo < m*n`：`target` 比所有元素大时行号越界。

**追问。**
- 只保证行列各自有序（LC 240）怎么做？：从右上角出发，大了左移、小了下移，`O(m+n)`。
- 能先二分行再二分列吗？：能，`O(log m + log n)`，同阶但边界更易写错。

**同模式。** LC 240 搜索二维矩阵 II、LC 704 二分查找、LC 35 搜索插入位置、LC 378 有序矩阵中第 K 小的元素
