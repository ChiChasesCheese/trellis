---
slug: sparse-matrix-multiplication
---
## Q
**LC 311 稀疏矩阵的乘法**｜Medium

给定稀疏矩阵 `mat1`（`m × k`）和 `mat2`（`k × n`），返回它们的乘积。

## A
**一句话。** 循环顺序改成 `i → k → j`，跳过 `mat1[i][k] == 0`，再只遍历 `mat2` 第 `k` 行预先压好的非零项。

**图解。** `i → k → j` 顺序：`mat1` 第 `i` 行的每个非零数，乘上 `mat2` 第 `k` 行的非零项，累加进结果第 `i` 行。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 165">
<rect x="16" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="42" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="68" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="16" y="56" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="29.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="42" y="56" width="26" height="26" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="55.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="68" y="56" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="108" y="64" text-anchor="middle" font-size="14" font-family="sans-serif" fill="currentColor">×</text>
<rect x="124" y="30" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="150" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="163.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="176" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="124" y="56" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="150" y="56" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="163.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="176" y="56" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="124" y="82" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="150" y="82" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="163.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="176" y="82" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="216" y="64" text-anchor="middle" font-size="14" font-family="sans-serif" fill="currentColor">=</text>
<rect x="232" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="258" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="284" y="30" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="47.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="232" y="56" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-7</text>
<rect x="258" y="56" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="284" y="56" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="55" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">mat1</text>
<text x="163" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">mat2</text>
<text x="271" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">res</text>
<text x="16" y="130" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">i = 1：k = 0，−1 × 第 0 行非零 (0, 7)</text>
<text x="16" y="150" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">k = 2，3 × 第 2 行非零 (2, 1)；k = 1 是 0，跳过</text>
</svg>

```python
def multiply(mat1, mat2):
    m, n = len(mat1), len(mat2[0])
    # mat2 每行压成 [(列, 值)]，只留非零
    rows2 = [[(j, b) for j, b in enumerate(r) if b]
             for r in mat2]
    res = [[0] * n for _ in range(m)]
    for i, row in enumerate(mat1):
        for k, a in enumerate(row):
            if a == 0:
                continue
            for j, b in rows2[k]:
                res[i][j] += a * b
    return res
```

**复杂度。** 时间 `O(mk + nnz1 · 平均每行非零数)`，空间 `O(mn)`。

**易错点。**
- 用 `[[0] * n] * m` 建结果：各行是同一个列表，改一行全变。
- 把累加写成赋值 `res[i][j] = a * b`：`[[1,1]] x [[1],[1]]` 得 `[[1]]`，应为 `[[2]]`。

**追问。**
- 输入本身是字典存非零项？：按行号给 `mat2` 分组，只遍历 `mat1` 的非零项，相消成 0 的要删。
- 两个矩阵稀疏程度不同？：把更稀疏的放外层。

**同模式。** LC 1570 两个稀疏向量的点积、LC 566 重塑矩阵、LC 54 螺旋矩阵、LC 48 旋转图像
