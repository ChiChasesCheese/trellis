---
id: uth-go-rust-go-slice-map-1-append
node: go-rust.go-slice-map
type: qa
step: 1
---
## Q
**append 的容量怎样增长**｜Go · 1.18 起

连续 `append` 一个 `[]int` 时，`cap` 每次翻倍吗？

## A
**背景。** 切片（slice）是数组的一扇“窗口”：记着指向底层数组的指针、当前长度和容量。长度追上容量时，`append` 只能新开一块更大的数组，把旧元素拷过去。每次只多一点，就要反复拷贝，所以必须按比例放大。

**结构。** 切片是“指针、长度、容量”三元组；容量不够时 `growslice` 新开一块、拷贝、换指针。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">连续 append, cap 的变化 (条长 = 容量)</text>
<rect x="10" y="28" width="23" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="39" y="41" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">256</text>
<rect x="10" y="52" width="46" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="62" y="65" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">512</text>
<text x="330" y="65" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×2.00</text>
<rect x="10" y="76" width="76.1875" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="92.1875" y="89" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">848</text>
<text x="330" y="89" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×1.66</text>
<rect x="10" y="100" width="115" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="131" y="113" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">1280</text>
<text x="330" y="113" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×1.51</text>
<rect x="10" y="124" width="161" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="177" y="137" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">1792</text>
<text x="330" y="137" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×1.40</text>
<rect x="10" y="148" width="230" height="18" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="246" y="161" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">2560</text>
<text x="330" y="161" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">×1.43</text>
<text x="8" y="188" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小于 256 翻倍; 之后每轮加 (cap+768)/4</text>
<text x="8" y="204" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">越大越接近 1.25 倍</text>
</svg>
```

**细节。**

- 旧容量小于 256：新容量翻倍
- 否则每轮加 `(cap + 768) / 4`，直到够用；越大越接近 1.25 倍
- 最后还要向上取整到内存分配器的规格（size class：分配器只提供固定的几档大小）
- 实测 `[]int`：`256 512 848 1280 1792 2560 3408 5120`

**为什么。** 小切片翻倍省拷贝；大切片翻倍会浪费很多内存，放缓增速让两者平滑过渡。

**对应 LeetCode：** 无直接对应的题（运行时的扩容策略）
