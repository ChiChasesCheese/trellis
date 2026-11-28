---
id: hi-sdx-cdn-shield-arithmetic
node: more.cdn-design
type: qa
step: 1
---
## Q
**中层缓存把源站 QPS 降到五分之一**｜补充 · 内容分发网络（CDN）设计 · 必会

面试官：「300 个边缘节点分成 15 个区域，每区一个中层缓存（origin shield）管 20 个边缘。峰值 1736 万 QPS，边缘命中率 95%，中层再吸收 80% 的边缘未命中。源站要扛多少 QPS？没有中层呢？流量再涨 10 倍呢？」

## A
**结论。** 有中层：17,361,111 × 5% × 20% ≈ 17.4 万 QPS；没有中层是 86.8 万，降到五分之一。但吸收的是比例而不是上限：流量涨 10 倍，源站也涨 10 倍，到约 174 万。

**要点。**
- **边缘未命中：** 1736 万 × 5% = 868,056 次/秒，没有中层时全部打到源站。
- **中层的作用：** 汇聚 20 个边缘，同一对象在多个边缘的未命中合并成一次回源，吸收 80%。
- **源站按残余定容量：** 剩下的 20% 是真正的冷内容或新内容，173,611 次/秒才是源站要扛的。
- **十倍流量：** 比例不变，源站涨到 1,736,111 次/秒，是原来容量的十倍。
- **怎么办：** 提高边缘和中层命中率（更大缓存、更长 TTL、统一缓存键、预热）；或再加一层跨区域汇聚；或扩源站。边缘未命中率从 5% 降到 4%，源站负载就少 20%。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<rect x="40" y="8" width="260" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">边缘 300 个</text>
<text x="170.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">峰值 17,361,111 /s</text>
<polyline points="170,46 170,68" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,68.0 173.2,61.0 166.8,61.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">边缘未命中 5%</text>
<rect x="40" y="68" width="260" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到达中层</text>
<text x="170.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">868,056 /s（无中层时全打源站）</text>
<polyline points="170,106 170,128" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,128.0 173.2,121.0 166.8,121.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">中层吸收 80%</text>
<rect x="40" y="128" width="260" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">源站</text>
<text x="170.0" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">173,611 /s</text>
<text x="10" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">流量涨 10 倍：比例不变，源站涨到约 174 万/s</text>
<text x="10" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要再降未命中率，或再加一层汇聚</text>
</svg>

**面试里这样说。** 「边缘未命中 5% 是 87 万/秒，中层再吸收 80%，源站剩 17 万/秒，是五倍。但这是比例，流量涨十倍源站也涨十倍，所以我会先抠命中率，不够再加一层汇聚。」

**易错。**
- **以为中层让源站压力归零：** 冷内容和新内容永远要回源。
- **按平均命中率线性外推：** 要按长尾和冷内容的残余来定源站容量。
