---
id: uth-storage-inverted-index-4-roaring-filter
node: storage.inverted-index
type: qa
step: 4
---
## Q
**过滤器缓存：Roaring 位图**｜Lucene · 10.5

查询里的过滤条件（如 `status:active`）会缓存成一个文档集合。怎么存才既省内存又能快速求交？

## A
**背景。** 同一个过滤条件会被反复用，命中的文档集合值得缓存。这个集合可能很稀疏（一百万篇里命中几篇），也可能很稠密，只用一种存法总有一头浪费。

**结构。** 查询缓存（`LRUQueryCache`）：命中文档占比达到 1% 用普通位图（`FixedBitSet`，每个文档一位），更稀疏的用 `RoaringDocIdSet`。Roaring 把文档号空间切成每块 65536 个，每块各选最省的格式。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 134">
<text x="170" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">文档号每 65536 个分一块, 各块自选容器</text>
<rect x="8" y="24" width="78" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="47" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数组</text>
<text x="47" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">至多 4096</text>
<text x="47" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有序 short[]</text>
<rect x="90" y="24" width="78" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="129" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位图</text>
<text x="129" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其余</text>
<text x="129" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8 KB 位图</text>
<rect x="172" y="24" width="78" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="211" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">反向数组</text>
<text x="211" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超 61440</text>
<text x="211" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存没命中的</text>
<rect x="254" y="24" width="78" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="293" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空</text>
<text x="293" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 个</text>
<text x="293" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不分配</text>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4096 个 short = 8 KB = 位图大小</text>
</svg>
```

**细节。**

- 命中不超过 4096 个，用有序的 `short[]`；超过 65536 − 4096 个，存“没命中的”那份 `short[]`；其余用位图。
- 完全没命中的块不分配空间。

**为什么。** 4096 个 `short` 正好 8 KB，和 65536 位的位图一样大：稀疏时数组更小，稠密时位图更小，4096 是两者相等的临界点。

**对应 LeetCode：** 无直接对应的题
