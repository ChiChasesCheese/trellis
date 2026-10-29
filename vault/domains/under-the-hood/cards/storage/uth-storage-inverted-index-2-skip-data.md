---
id: uth-storage-inverted-index-2-skip-data
node: storage.inverted-index
type: qa
step: 2
---
## Q
**跳转数据：求交集时跳着走**｜Lucene · 10.5

一个词的文档号列表有几百万项，另一个词只有几十项，求交集时 Lucene 怎么避免把长列表扫一遍？

## A
**背景。** 双指针每次只往前走一步。长列表有几百万项，短列表只有几十项，却要把长列表整个走一遍，太浪费。

**结构。** 长列表里夹着两级跳转数据（skip data）：第 0 级在每个 256 项的块之前，第 1 级每 32 个块一条，覆盖 8192 篇文档。求交集时以最短的列表为主，对其他列表说“直接跳到不小于这个文档号的位置”（`advance(目标文档号)`）：先用第 1 级跳过整段 8192 篇，再用第 0 级跳过块，最后只解码一个块。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 146">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 1 级: 每条覆盖 32 块 = 8192 篇</text>
<rect x="12" y="20" width="100" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8192 篇</text>
<rect x="118" y="20" width="100" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="168" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8192 篇</text>
<rect x="224" y="20" width="100" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="274" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8192 篇</text>
<line x1="62" y1="44" x2="62" y2="56" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="62" y1="56" x2="258" y2="56" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="258" y1="56" x2="258" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258,90 255.0,84.0 261.0,84.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">跳过整段</text>
<rect x="12" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="38" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="64" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="90" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="116" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="142" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="168" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="220" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="246" y="92" width="24" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="272" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="298" y="92" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只解码目标所在的那一块</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 级: 每块 256 篇</text>
</svg>
```

**细节。**

- 以最短的列表为主驱动（`ConjunctionDISI` 按成本排序）。
- 对方跳过头了，主列表就跟着往前跳（leapfrog，蛙跳）。

**为什么。** 跳转数据就是磁盘版的跳表（分层的有序链表，上层一次跨多项）：求交集的代价由短列表的长度决定，不由长列表的长度决定。

**对应 LeetCode：** 无直接对应的题
