---
slug: range-sum-query-2d-immutable
---
## Q
**LC 304 二维区域和检索 - 矩阵不可变**｜Medium

给定不变的矩阵，多次查询子矩形 `(r1, c1)` 到 `(r2, c2)` 的元素和，每次查询要 `O(1)`。

## A
**一句话。** 预处理二维前缀和 `P[i][j]`（左上 `i` 行 `j` 列之和），查询用容斥：大块减上、减左、加回左上。

**图解。** 二维前缀和的容斥：整块减上、减左，被减了两次的左上角加回一次。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="20" y="20" width="150" height="60" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="20" width="60" height="150" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="20" width="60" height="60" rx="0" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="80" width="90" height="90" rx="0" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<line x1="20" y1="20" x2="20" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="20" x2="170" y2="20" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="50" y1="20" x2="50" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="50" x2="170" y2="50" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="80" y1="20" x2="80" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="80" x2="170" y2="80" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="110" y1="20" x2="110" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="110" x2="170" y2="110" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="140" y1="20" x2="140" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="140" x2="170" y2="140" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="20" x2="170" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<line x1="20" y1="170" x2="170" y2="170" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<rect x="20" y="20" width="150" height="150" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">角</text>
<text x="125.0" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上</text>
<text x="50" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">左</text>
<text x="125.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="600">所求</text>
<text x="186" y="34" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">所求 = 全 − 上 − 左 + 角</text>
<text x="186" y="62" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">全 = P[r2+1][c2+1]</text>
<text x="186" y="84" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">上 = P[r1][c2+1]</text>
<text x="186" y="106" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">左 = P[r2+1][c1]</text>
<text x="186" y="128" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">角 = P[r1][c1]</text>
<text x="186" y="160" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">角被减了两次，加回一次</text>
<text x="95.0" y="186" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全 = 左上角到右下角整块</text>
</svg>

```python
class NumMatrix:
    def __init__(self, matrix):
        m, n = len(matrix), len(matrix[0])
        # 多一行一列，免判边界
        self.P = P = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                P[i+1][j+1] = (P[i][j+1] + P[i+1][j]
                               - P[i][j] + matrix[i][j])

    def sumRegion(self, r1, c1, r2, c2):
        P = self.P
        return (P[r2+1][c2+1] - P[r1][c2+1]
                - P[r2+1][c1] + P[r1][c1])
```

**复杂度。** 预处理时间 `O(mn)`，查询 `O(1)`；空间 `O(mn)`。

**易错点。**
- 下标错位：`P` 比矩阵多一行一列，查询右下角要用 `r2+1, c2+1`，左上用 `r1, c1`。
- 建表漏减 `P[i][j]`：上和左都含左上角那块，加了两次要减一次。

**追问。**
- 矩阵很大，怎么多线程算前缀和？：分两阶段：先每行各自做行前缀（行与行无依赖，按行分给线程），屏障（barrier）同步后再每列做列前缀（按列分给线程）。CPython 有 GIL，纯 Python 线程不会变快：用 numpy 的 `cumsum(axis=1)` 再 `cumsum(axis=0)`（C 循环，按行块分给线程时可并行），或多进程加共享内存。
- 按块切给线程怎么做？：每块先算块内前缀，再加上方块最后一行和左方块最后一列传来的偏移；块间只传边界，适合多机或 GPU。
- 矩阵会被修改？：前缀和单点更新要 `O(mn)`；改用二维树状数组（Fenwick Tree），更新和查询都 `O(log m · log n)`。

**同模式。** LC 560 和为 K 的子数组、LC 303 区域和检索 - 数组不可变、LC 1314 矩阵区域和
