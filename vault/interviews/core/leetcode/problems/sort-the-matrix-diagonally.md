---
slug: sort-the-matrix-diagonally
---
## Q
**LC 1329 将矩阵按对角线排序**｜Medium

把 `m × n` 矩阵每条左上到右下的对角线各自升序排序，返回结果矩阵。

## A
**一句话。** 同一条对角线上 `i - j` 相同；按 `i - j` 分组收集、排序，再按原顺序填回。

**图解。** 格中是 `i - j`，相同的数在同一条对角线上，例如深色是 `0`、浅色是 `-1`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160">
<rect x="26" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="56" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="116" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="26" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="56" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="116" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="26" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="56" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="116" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">格中是 i - j：相同即同一条对角线</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色 i-j = 0，浅色 i-j = -1</text>
</svg>

```python
def diagonal_sort(mat):
    m, n = len(mat), len(mat[0])
    diag = defaultdict(list)   # i - j -> 这条对角线的值
    for i in range(m):
        for j in range(n):
            diag[i - j].append(mat[i][j])
    for d in diag.values():
        d.sort(reverse=True)   # 倒序，pop() 从小到大取
    for i in range(m):
        for j in range(n):
            mat[i][j] = diag[i - j].pop()
    return mat
```

**复杂度。** 时间 `O(mn log min(m, n))`，空间 `O(mn)`。

**易错点。**
- 用 `i + j` 分组：那是反对角线（右上到左下）。
- 升序排序后 `pop()`：从末尾取出的是最大值，填进去变成降序。

**追问。**
- 值域只有 1 到 100？：每条对角线用计数排序，`O(mn + 100·(m+n))`。
- 不开字典？：从第一行、第一列的每个起点出发，沿对角线取出、排序、写回。

**同模式。** LC 48 旋转图像、LC 498 对角线遍历、LC 1424 对角线遍历 II
