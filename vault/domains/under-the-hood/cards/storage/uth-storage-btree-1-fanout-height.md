---
id: uth-storage-btree-1-fanout-height
node: storage.btree
type: qa
step: 1
---
## Q
**扇出与高度：三四层装下亿行**｜InnoDB · MySQL 8.4

B+ 树为什么三四层就能存下上亿行？InnoDB 的一个内部页能放多少个子指针？

## A
**背景。** 数据库在磁盘上找一行，慢的是读盘；磁盘每次最少读一页（InnoDB 默认 16 KB，`innodb_page_size`）。用二叉搜索树（每个节点两个孩子）在一百万行里找一行，要走约 20 层，也就是约 20 次读盘。

**结构。** B+ 树把每个节点做成恰好一页，里面不放两个指针，而放几百个：内部页只放“键 + 子页号”，整行只放在最底下的叶子页。一页能指向的孩子个数叫扇出（fanout）。扇出约 900，高度就从 20 层降到 3 层：每层读一页，找一行只要读 3 页。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<text x="8" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 页</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 900 页</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 81 万页</text>
<rect x="168" y="22" width="64" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="200" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根</text>
<rect x="86" y="76" width="64" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="118" y="93.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内部页</text>
<rect x="168" y="76" width="64" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="93.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内部页</text>
<rect x="250" y="76" width="64" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="93.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内部页</text>
<line x1="200" y1="48" x2="118" y2="76" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="200" y1="48" x2="200" y2="76" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="48" x2="282" y2="76" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="142" y="132" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="149.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶</text>
<line x1="200" y1="102" x2="160" y2="132" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="182" y="132" width="36" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="200" y="149.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶</text>
<line x1="200" y1="102" x2="200" y2="132" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="222" y="132" width="36" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="149.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶</text>
<line x1="200" y1="102" x2="240" y2="132" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="200" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个叶页约 15 行</text>
</svg>
```

**细节。**

- bigint 主键的内部页记录 = 8 字节键 + 4 字节页号 + 5 字节记录头 = 17 字节，一页扇出约 900（估算）。
- 1 KB 的行一页放约 15 行：3 层约 900² × 15 ≈ 1200 万行，4 层约 100 亿行（估算）。

**为什么。** 把节点做得和磁盘页一样大，用宽度换高度，读盘次数就少了。

**例题：** LC 74 搜索二维矩阵

`m x n` 矩阵每行非递减，且每行首元素大于上一行末元素；判断 `target` 是否在矩阵中，要求 O(log(m * n))。例：`matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]`，`target = 3` → `true`；`target = 13` → `false`。

```python
def search_matrix(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n                      # 把矩阵按行拼成一维有序数组，二分的区间是 [lo, hi)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        row, col = divmod(mid, n)          # 一维下标 -> 行、列
        if matrix[row][col] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < m * n and matrix[lo // n][lo % n] == target
```
