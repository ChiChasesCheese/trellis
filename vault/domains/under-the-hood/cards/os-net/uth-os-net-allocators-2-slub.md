---
id: uth-os-net-allocators-2-slub
node: os-net.allocators
type: qa
step: 2
---
## Q
**kmalloc 为什么有 96 和 192 这两档**｜Linux · SLUB · 内核 7.3

内核里 `kmalloc(100)` 实际占多少字节？成千上万个小对象怎样避免碎片？

## A
**背景。** 伙伴系统以页（4 KB）为单位，可内核常常只要几十上百字节（比如一个文件结构）。每次给一整页太浪费；按原样切小又会留下形状各异的空洞。slab 分配器的办法：向伙伴系统要来整页，切成大小相同的格子，一页只放一种对象；申请就拿一格，释放就还一格。

**结构。** 每种大小一个缓存（名字像 `kmalloc-128`），缓存里是若干 slab 页。内核 7.3 里 slab 分配器只剩 SLUB 一种实现。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="20" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">kmalloc 大小档</text>
<rect x="19" y="26" width="54" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">64</text>
<rect x="81" y="26" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="108" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">96</text>
<rect x="143" y="26" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">128</text>
<rect x="205" y="26" width="54" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="232" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">192</text>
<rect x="267" y="26" width="54" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">256</text>
<line x1="108" y1="80" x2="108" y2="59" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M108.0,54.0 L111.3,60.8 L104.7,60.8 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="108" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">65 字节</text>
<line x1="170" y1="80" x2="170" y2="59" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,54.0 L173.3,60.8 L166.7,60.8 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="178" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">100 字节</text>
<text x="20" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">一页 slab 切成同样大的对象</text>
<rect x="38" y="140" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已用</text>
<rect x="82" y="140" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">空闲</text>
<rect x="126" y="140" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="148" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已用</text>
<rect x="170" y="140" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="192" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">空闲</text>
<rect x="214" y="140" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="236" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">空闲</text>
<rect x="258" y="140" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="280" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">已用</text>
<path d="M104,166 Q148,186 187.4,168.1" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M192.0,166.0 L187.2,171.8 L184.5,165.8 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<path d="M192,166 Q214,182 232.0,168.9" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M236.0,166.0 L232.5,172.6 L228.6,167.3 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">空闲格子体内存着下一个空闲格子的指针</text>
</svg>
```

**细节。**

- `kmalloc` 的大小档有 64、96、128、192、256、512 …，请求向上取整到最近一档
- 100 字节落到 128 档；65 字节落到 96 档，只浪费 31 字节而不是 63
- 空闲格子把“下一个空闲格子的指针”存在自己体内，空闲链表不占额外内存

**为什么。** 同尺寸的格子释放后原样复用，不产生外部碎片；多加 96 和 192 两档，是为了让中间尺寸少浪费。

**对应 LeetCode：** 无直接对应的题
