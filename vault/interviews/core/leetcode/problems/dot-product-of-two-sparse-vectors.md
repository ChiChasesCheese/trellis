---
slug: dot-product-of-two-sparse-vectors
---
## Q
**LC 1570 两个稀疏向量的点积**｜Medium

实现 `SparseVector(nums)` 与 `dotProduct(vec)`，高效存储绝大多数分量为 `0` 的向量并求点积。

## A
**一句话。** 只存非零分量的 `下标 -> 值` 字典，点积时遍历非零更少的一个，到另一个里查同一下标。

**图解。** 只存非零分量，遍历较小的字典，到另一个里按下标查。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 175">
<text x="76" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="108" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="140" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="172" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="204" y="14" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="60" y="20" width="32" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="76.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="20" width="32" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="108.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="124" y="20" width="32" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="156" y="20" width="32" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="172.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="188" y="20" width="32" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="204.0" y="37.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="60" y="56" width="32" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="92" y="56" width="32" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="108.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="124" y="56" width="32" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="156" y="56" width="32" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="172.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="188" y="56" width="32" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="204.0" y="73.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="52" y="37" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v1</text>
<text x="52" y="73" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v2</text>
<text x="20" y="110" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">nz1 = {0: 1, 3: 2, 4: 3}</text>
<text x="20" y="130" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">nz2 = {1: 3, 3: 4}  ← 更小，遍历它</text>
<text x="20" y="156" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下标 1 不在 nz1；下标 3：4 × 2 = 8</text>
</svg>

```python
class SparseVector:
    def __init__(self, nums):
        self.nz = {i: x for i, x in enumerate(nums) if x}

    def dotProduct(self, vec):
        a, b = sorted((self.nz, vec.nz), key=len)
        return sum(x * b[i] for i, x in a.items() if i in b)
```

**复杂度。** 时间 构造 `O(n)`，点积 `O(min(L1, L2))`（`L` 为非零个数），空间 `O(L)`。

**易错点。**
- 遍历较大的向量去查较小的：变成 `O(max(L1, L2))`。
- 把零值也存进字典：失去稀疏的意义，用 `if x` 过滤。
- 直接 `b[i]` 不判断存在：`a` 的下标在 `b` 里可能没有，`KeyError`。

**追问。**
- 只有一个向量稀疏怎么办？：遍历稀疏的那个，对稠密数组按下标直接取，`O(L)`。
- 两个向量都有序存成 `(下标, 值)` 列表呢？：双指针归并，`O(L1 + L2)`，也可对较大者二分。

**同模式。** LC 311 稀疏矩阵的乘法、LC 986 区间列表的交集、LC 349 两个数组的交集
