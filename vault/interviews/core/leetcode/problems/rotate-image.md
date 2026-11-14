---
slug: rotate-image
---
## Q
**LC 48 旋转图像**｜Medium

把 `n × n` 矩阵原地顺时针旋转 90 度。

## A
**一句话。** 顺时针 90 度 = 先沿主对角线转置，再把每一行左右翻转。

**图解。** 先沿主对角线转置，再把每行左右翻转，就是顺时针转 90 度。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 125">
<rect x="10" y="20" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="22.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="34" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="58" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="10" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="34" y="44" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="58" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="10" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="34" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="58" y="68" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<polyline points="88,56 108,56" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="108.0,56.0 102.0,59.0 102.0,53.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="114" y="20" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="138" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="162" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="114" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="138" y="44" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="162" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="114" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="138" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="162" y="68" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<polyline points="192,56 212,56" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212.0,56.0 206.0,59.0 206.0,53.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="218" y="20" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="242" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="266" y="20" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="36.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="218" y="44" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="242" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="266" y="44" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="60.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="218" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="242" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="266" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="84.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="46" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原矩阵</text>
<text x="150" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">沿对角线转置</text>
<text x="254" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每行反转</text>
</svg>

```python
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):     # 只换上三角
            a = matrix
            a[i][j], a[j][i] = a[j][i], a[i][j]
    for row in matrix:
        row.reverse()
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`。

**易错点。**
- 转置内层从 `0` 开始：每对被换两次，等于没转置。内层要从 `i + 1` 起。
- `matrix = [list(r) for r in zip(*matrix[::-1])]`：只改了局部变量，调用方矩阵不变，要写 `matrix[:] = ...`。
- 两步顺序反了：先翻行再转置得到逆时针。

**追问。**
- 逆时针 90 度？：先转置，再 `matrix.reverse()` 倒转行序。
- 非方阵 `m × n`？：形状变了不能原地，返回 `[list(r) for r in zip(*matrix[::-1])]`。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 867 转置矩阵、LC 73 矩阵置零
