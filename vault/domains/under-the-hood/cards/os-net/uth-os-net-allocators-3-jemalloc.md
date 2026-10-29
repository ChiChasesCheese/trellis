---
id: uth-os-net-allocators-3-jemalloc
node: os-net.allocators
type: qa
step: 3
---
## Q
**jemalloc 的尺寸分级**｜jemalloc · 5.3.0

`malloc(130)` 在 jemalloc 里实际占多少字节？分档为什么是“每翻一倍分 4 档”？

## A
**背景。** 用户程序的 `malloc` 同样面对碎片：请求大小五花八门，释放后留下形状各异的洞。jemalloc 先把请求取整到有限的几档（尺寸分级，size class），每档用专门的页（slab）切成同样大的格子，同档的格子可以互相顶替。分得太粗浪费大，分得太细档数多，每档都要留一批空闲页。

**结构。** 以 64 位、16 字节对齐为例：16 一档排到 128，之后 160、192、224、256，再 320、384、448、512 ……每翻一倍分 4 档。slab 内用一张位图（每格一位）记录哪些格子在用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="14" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="31" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">128</text>
<rect x="50" y="60" width="34" height="26" rx="2" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="67" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">160</text>
<rect x="86" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="103" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">192</text>
<rect x="122" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">224</text>
<rect x="158" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">256</text>
<rect x="194" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="211" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">320</text>
<rect x="230" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">384</text>
<rect x="266" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="283" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">448</text>
<rect x="302" y="60" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="319" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">512</text>
<line x1="50" y1="100" x2="192" y2="100" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="122" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">每翻一倍 4 档</text>
<line x1="194" y1="100" x2="336" y2="100" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="266" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">每翻一倍 4 档</text>
<text x="32" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">130 字节</text>
<path d="M40,32 Q53.5,45 63.4,54.5" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M67.0,58.0 L59.9,55.7 L64.4,51.0 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">取不小于请求的最小一档 浪费 30 字节</text>
</svg>
```

**细节。**

- 130 字节取整到 160，浪费 30 字节；除最小几档外，浪费不超过约 20%
- 每个线程有自己的小缓存（`tcache`），默认缓存到 32 KiB 的档：线程先从自己手里拿格子，不用和别的线程抢锁

**为什么。** 纯 2 的幂分档最坏浪费近一半，每倍分 4 档把上限压到约 20%，档数仍然很少。

**例题：** LC 35 搜索插入位置

给定升序、无重复元素的数组 `nums` 和目标值 `target`：找到就返回下标，找不到就返回它应当插入的位置，要求 O(log n)。例：`nums=[1,3,5,6]`，`target=2` → 1。

```python
import bisect

def search_insert(nums: list[int], target: int) -> int:
    return bisect.bisect_left(nums, target)
```
