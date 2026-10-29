---
id: uth-os-net-allocators-1-buddy
node: os-net.allocators
type: qa
step: 1
---
## Q
**内核怎样快速分出连续的页**｜Linux · 页分配器 · 内核 6.12 与 7.3

程序要 4 页连续内存，空闲页零零散散，内核怎样又快又少碎片地分出来？

## A
**背景。** 分配器要回答：要 n 块连续内存，从哪里切？最直接的办法是把空闲区间排成一张表，每次从头找第一块够大的。毛病有两个：要扫表；切来切去，空闲内存碎成许多小块，总量够却凑不出一大块（外部碎片）。伙伴系统（buddy system）的办法：块的大小只能是 2 的幂，只能对半切、对半合。

**结构。** 空闲页按阶（order）挂在 0 到 10 共 11 条链表上，第 k 阶的块是 2^k 个连续页。例：要 4 页（2 阶），只剩一块 8 页（3 阶）：对半切，`pfn` 0 起的 4 页给你，另外 4 页放回 2 阶链表。释放时反过来：两半都空闲，就并回 8 页。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="98" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">k=2 块 pfn 0</text>
<text x="242" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">伙伴 pfn 4</text>
<rect x="26" y="34" width="144" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="170" y="34" width="144" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="62" y1="34" x2="62" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="98" y1="34" x2="98" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="134" y1="34" x2="134" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="170" y1="34" x2="170" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="206" y1="34" x2="206" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="242" y1="34" x2="242" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="278" y1="34" x2="278" y2="60" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="44" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0</text>
<text x="80" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">1</text>
<text x="116" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">2</text>
<text x="152" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">3</text>
<text x="188" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4</text>
<text x="224" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">5</text>
<text x="260" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">6</text>
<text x="296" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">7</text>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">0 ^ (1 &lt;&lt; 2) = 4</text>
<line x1="170" y1="112" x2="170" y2="125" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,130.0 L166.7,123.2 L173.3,123.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="26" y="134" width="288" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">两块都空闲 合并成 k=3 块 pfn 0</text>
</svg>
```

**细节。**

- 页框号（`pfn`，物理页的编号）为 `pfn` 的 k 阶块，另一半（伙伴）的编号是 `pfn ^ (1 << k)`，例如 0 号 2 阶块的伙伴是 4 号
- 释放时伙伴也空闲就合并成 k+1 阶，一路合并到最高阶 10（4 KB 页下是 4 MB）；合并后的起点是 `buddy_pfn & pfn`

**为什么。** 大小和位置都按 2 的幂对齐，找伙伴、合并只是一次位运算，不用扫表；代价是请求 5 页也只能拿 8 页，多出的 3 页浪费（内部碎片）。

**例题：** LC 2502 设计内存分配器

设计内存分配器：`Allocator(n)` 管理 n 个内存单元；`allocate(size, mID)` 找最左边连续 `size` 个空闲单元，分配给 `mID` 并返回起点，没有则返回 -1；`freeMemory(mID)` 释放该 `mID` 的所有单元并返回个数。n、size、mID 都不超过 1000。例：n=10，`allocate(1,1)` → 0，`allocate(1,2)` → 1，`freeMemory(1)` → 1。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n             # mem[i] 是占用该单元的 mID；mID >= 1，所以 0 表示空闲

    def allocate(self, size: int, mID: int) -> int:
        run = 0                        # 当前连续空闲单元的个数
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:            # 第一次凑够 size 个，就是最左侧的块
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size   # 切片赋值，一次写入整块
                return start
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:           # 同一个 mID 可能分散在多个块里，全部释放
                self.mem[i] = 0
                freed += 1
        return freed
```
