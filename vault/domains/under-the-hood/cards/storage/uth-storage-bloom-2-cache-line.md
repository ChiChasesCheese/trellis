---
id: uth-storage-bloom-2-cache-line
node: storage.bloom
type: qa
step: 2
---
## Q
**缓存行内探测与 Ribbon 过滤器**｜RocksDB · v10.9

经典布隆过滤器的 k 次探测落在内存的 k 个不同位置，每次都可能 cache miss。RocksDB 怎么改？

## A
**背景。** CPU 读内存是一次读一整个缓存行（64 字节）。要的位置不在缓存里，就得停下来等内存（cache miss），很慢。经典做法的 k 个位置散在整个位数组里，最坏要等 k 次。

**结构。** 现代 RocksDB 的布隆过滤器先用一次哈希选定一个 64 字节（512 位）的缓存行，k 次探测全落在这一行里，一次内存访问就够。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 156">
<text x="12" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">经典: 6 次探测落在 6 处</text>
<rect x="12" y="28" width="316" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="40" y1="22" x2="40" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="95" y1="22" x2="95" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="140" y1="22" x2="140" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="22" x2="200" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="255" y1="22" x2="255" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="300" y1="22" x2="300" y2="54" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="12" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">6 次 cache miss</text>
<text x="12" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RocksDB: 先选一个 64 字节缓存行</text>
<rect x="12" y="110" width="316" height="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="110" width="44" height="20" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="175" y1="106" x2="175" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="181" y1="106" x2="181" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="189" y1="106" x2="189" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="196" y1="106" x2="196" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="204" y1="106" x2="204" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="209" y1="106" x2="209" y2="134" stroke="currentColor" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="192" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 次 cache miss</text>
</svg>
```

**细节。**

- 10 位/key、6 次探测、512 位的桶：理论最优误判率 0.9535%，实现约 0.957%（旧的缓存局部实现是 1.138%）。
- Ribbon 过滤器（6.15 起，一种更省空间、构造更费 CPU 的替代结构）：同样约 1% 误判只用约 7 位/key，省约 30% 内存，构造时 CPU 约 3–4 倍。

**为什么。** 过滤器的瓶颈是内存访问而不是计算：限制在一个缓存行内，误判率几乎不变，cache miss 从 k 次降到 1 次。

**对应 LeetCode：** 无直接对应的题
