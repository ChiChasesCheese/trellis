---
slug: set-matrix-zeroes
---
## Q
**LC 73 矩阵置零**｜Medium

`m × n` 矩阵中某元素为 `0`，就把它所在的整行整列设为 `0`，要求原地。

## A
**一句话。** 用首行首列当标记，另用两个布尔值记首行首列自己原本有没有 `0`。

**图解。** 首行首列当记事本：原有的 0 把标记写到行首和列首，再按标记置零。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 140">
<rect x="14" y="20" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="40" y="20" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="66" y="20" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="20" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="14" y="46" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="40" y="46" width="26" height="26" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="66" y="46" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="46" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="14" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="40" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="66" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="72" width="26" height="26" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<polyline points="130,59 156,59" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="156.0,59.0 150.0,62.0 150.0,56.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="166" y="20" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="192" y="20" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="218" y="20" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="244" y="20" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="166" y="46" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="192" y="46" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="218" y="46" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="244" y="46" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="63.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="166" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="192" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="218" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="231.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="244" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="89.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="66" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">记到首行首列</text>
<text x="218" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按标记置零</text>
<text x="145" y="134" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">灰：原有的 0　深色：标记 / 置零</text>
</svg>

```python
def set_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = 0 in matrix[0]                  # 首行原本有 0
    col0 = any(r[0] == 0 for r in matrix)  # 首列原本有 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:          # 记在首行首列
                matrix[i][0] = matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        matrix[0][:] = [0] * n
    if col0:
        for r in matrix:
            r[0] = 0
```

**复杂度。** 时间 `O(mn)`，额外空间 `O(1)`。

**易错点。**
- 边扫边清零：新产生的 `0` 被当成原有的继续扩散，`[[0,1,1],[1,1,1],[1,1,1]]` 会变全 `0`。
- 没先记首行首列是否原有 `0`：标记会覆盖它们，`[[1,0],[1,1]]` 得 `[[0,0],[0,0]]`，应为 `[[0,0],[1,0]]`。
- 先清首行首列：标记被抹掉，内部格子没依据，它们必须最后处理。

**追问。**
- 不要求 `O(1)` 空间怎么做？：用两个集合记要清零的行和列，空间 `O(m + n)`，再统一清零。

**同模式。** LC 289 生命游戏、LC 48 旋转图像、LC 54 螺旋矩阵、LC 1706 球会落何处
