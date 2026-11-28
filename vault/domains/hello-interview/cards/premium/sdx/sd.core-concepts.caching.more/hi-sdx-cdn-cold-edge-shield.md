---
id: hi-sdx-cdn-cold-edge-shield
node: sd.core-concepts.caching.more
type: qa
step: 7
---
## Q
**全球同时发布保护源站**｜补充 · 缓存 · 追问

一部新片在全球午夜同时上线，200 个边缘节点的缓存全是冷的，观众瞬间涌入。拉模式（pull）CDN 会怎样？怎么保护源站？

## A
**结论。** 每个边缘节点各 miss 一次，同一个对象会回源 200 次以上。用中层缓存（origin shield）加请求合并把它压成 1 次，已知的热门发布再提前预热。

**要点。**
- **拉模式的冷启动：** 边缘被请求时才回源取。200 个节点各 miss 一次；节点内若不合并，同一时刻的并发请求还会各回源一次。
- **请求合并：** 每个节点（和中层）内，同一对象的并发 miss 只放一个出去，其余等结果。
- **中层缓存：** 所有边缘的 miss 先汇到一层或少数几个中层缓存，只有它回源：200 次变成 1 次。
- **推送或预热：** 发布时间已知，就提前把文件推到边缘，或预先请求一遍。长尾目录（几百万个几乎没人看的文件）不要推，会浪费边缘存储。

**为什么。** 源站承受的是「节点数 × 每点一次 miss」。加一层汇聚点，把乘法变成加法。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 264">
<rect x="8" y="8" width="100" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">边缘 1</text>
<polyline points="58,38 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 163.0,92.0 165.6,86.5" style="fill:var(--accent,#3b6fd4)"/>
<rect x="120" y="8" width="100" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">边缘 2</text>
<polyline points="170,38 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 167.0,85.7 173.0,85.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="232" y="8" width="100" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">… 共 200</text>
<polyline points="282,38 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 174.4,86.5 177.0,92.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="70" y="92" width="200" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中层缓存（shield）</text>
<text x="170" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合并并发请求</text>
<polyline points="170,136 170,184" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,184 167.0,177.7 173.0,177.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">200 次 → 1 次</text>
<rect x="95" y="184" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="205" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">源站</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">边缘各自是冷的，每处都会 miss；</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提前预热则首批请求直接命中。</text>
</svg>

**面试里这样说。** 「全球同时发布，我会在边缘和源站之间加一层 origin shield 并开请求合并，把 200 个边缘的 miss 合成一次回源，并对这部片提前预热；长尾素材不预热，按需拉取。」

**易错。**
- **只预热不做合并：** 预热名单之外的突发热点照样会踩踏源站。
- **全量推送：** 长尾对象占满边缘存储，命中率反而下降。
- **中层缓存成为新瓶颈：** 它要有降级路径，挂了能让边缘直接回源。
