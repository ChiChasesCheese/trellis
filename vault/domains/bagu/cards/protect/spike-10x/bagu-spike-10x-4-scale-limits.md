---
id: bagu-spike-10x-4-scale-limits
node: a.protect.spike-10x
type: qa
step: 4
---
## Q
**QPS 突增十倍 · 扩容的限制是什么，为什么不能只靠自动扩缩容**｜追问

面试官：「那我们直接开自动扩缩容，实例从 20 个涨到 130 个，不就解决了吗？」

## A
**基本回答。** 不够。自动扩缩容有冷启动（从触发、拉镜像、启动到预热要几分钟，指标也滞后，扩出来时峰值可能已过），救不了秒级突发；只有无状态应用能水平扩，数据库有状态，临时加几台解决不了；瓶颈会转移，应用扩得越大压向数据库、缓存、第三方的流量越大。数据库连接数 = 实例数 × 单实例连接池，实例翻几倍先撑爆库连接。已知活动（大促、开票）要提前扩容并预热缓存和连接；容量取压测拐点的约 70%。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间：扩容来不及</text>
<line x1="14" y1="44" x2="326" y2="44" stroke-width="1.2" stroke="currentColor"/>
<circle cx="14" cy="44" r="4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<circle cx="250" cy="44" r="4" fill="currentColor"/>
<text x="14" y="34" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 秒</text>
<text x="14" y="64" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">流量冲到 10 万</text>
<text x="250" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">几分钟后</text>
<text x="250" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新实例才就绪</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">空档只能靠限流、缓存、降级顶住</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">连接数：扩应用先撑爆库</text>
<rect x="8" y="136" width="84" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="152.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">130 个实例</text>
<text x="50.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（原来 20）</text>
<text x="100" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">×</text>
<rect x="108" y="136" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="144.0" y="152.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每实例</text>
<text x="144.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接池 20</text>
<text x="188" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">=</text>
<rect x="196" y="136" width="70" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="231.0" y="152.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2600</text>
<text x="231.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">个连接</text>
<line x1="266" y1="156" x2="276" y2="156" stroke-width="1.2" stroke="currentColor"/>
<polygon points="276.0,156.0 269.0,152.8 269.0,159.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="278" y="136" width="54" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305.0" y="152.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库上限</text>
<text x="305.0" y="167.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">够吗？</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">单实例 1000 QPS：10 万需 100 个，</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">留 30% 余量就是 130 个</text>
</svg>
上半是时间轴：峰值到来和新实例就绪之间有空档，只能靠限流、缓存、降级顶；下半是连接数相乘。
**业务场景。** 目标 10 万 QPS、单实例 1000 QPS 要 100 个，留 30% 余量 130 个（原来 20 个）；每实例连接池 20，130 × 20 = 2600 个连接涌向库，假设库最大连接数 1000，就超了 2.6 倍，新连接排队拒绝，整体反而更慢。一条短链接被大号转发后爆红就是这样；补救是热点链接走本地缓存加 Redis，并给每个实例设连接预算（池调小）。
**容易错。**
- **以为开自动扩缩容就万事大吉。**
- **只算实例数不算连接数：** 要把实例数 × 连接池和库最大连接数对账。
- **容量按 100% 用满规划。**
