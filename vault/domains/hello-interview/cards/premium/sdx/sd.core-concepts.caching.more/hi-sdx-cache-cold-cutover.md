---
id: hi-sdx-cache-cold-cutover
node: sd.core-concepts.caching.more
type: qa
step: 4
---
## Q
**新缓存集群怎么安全切流**｜补充 · 缓存 · 追问

要把读流量切到一套全新的缓存集群，它一开始是空的。读 5 万 QPS，稳态命中率 95%，数据库平时 2500 QPS、最多 1 万。直接切会怎样？怎么切才安全？

## A
**结论。** 直接切会让数据库瞬间承受 5 万 QPS，是上限的 5 倍。要先把新缓存填热，再按数据库的余量分步放量。

**要点。**
- **直接切的后果：** 新集群命中率为 0，5 万次读全落到数据库，冲破 1 万的上限。
- **先填热：** 重放热键日志，或从旧集群快照复制热门条目，这样不占数据库。
- **镜像要限速：** 把线上读复制给新集群时，它的 miss 同样会回源。只镜像一小部分，或让新集群从旧集群而不是数据库回填。
- **按余量放量：** 数据库读 = 2500×(1−s) + 5 万×s×(1−h)，s 是切过去的比例，h 是新集群命中率。留 20% 余量（≤ 8000）：切 10% 不需要预热；25% 要 h ≥ 51%；50% 要 h ≥ 73%；全量要 h ≥ 84%。

**为什么。** 新缓存的命中率是慢慢长出来的。数据库余量 1 万 − 2500 = 7500，就是你能承受的「额外 miss」预算，放量速度必须让额外 miss 不超过它。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每一步的数据库每秒读次数</text>
<text x="4" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次切 100%</text>
<text x="4" y="59" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率 0</text>
<rect x="92" y="34" width="190" height="26" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="98" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">50,000</text>
<text x="4" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先切 10%</text>
<text x="4" y="95" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率 0</text>
<rect x="92" y="70" width="114.792" height="26" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="88" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">7,250</text>
<text x="4" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再到 25%</text>
<text x="4" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率≥51%</text>
<rect x="92" y="106" width="126.667" height="26" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">8,000</text>
<text x="4" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再到 50%</text>
<text x="4" y="167" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率≥73%</text>
<rect x="92" y="142" width="126.667" height="26" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">8,000</text>
<text x="4" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">全量</text>
<text x="4" y="203" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中率≥84%</text>
<rect x="92" y="178" width="126.667" height="26" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">8,000</text>
<line x1="250.333" y1="26" x2="250.333" y2="208" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="250.333" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限 10,000</text>
</svg>

**面试里这样说。** 「新集群我不直切。先用旧集群的热键预热，再按数据库余量分步放量：先切 10%，命中率到 51% 放到 25%，一路到 84% 才全量，每一步数据库都保持在 8000 以内。」

**易错。**
- **把全部读流量镜像给新缓存：** 新缓存的 miss 也要回源，等于提前把数据库打满。
- **按时间表放量，不看命中率：** 命中率没长上来就放量，照样冲穿数据库。
- **全量后立刻下线旧集群：** 出问题时没有回退的地方。
