---
id: hi-sdx-cache-node-loss
node: sd.core-concepts.caching.more
type: qa
step: 3
---
## Q
**缓存挂一个节点冲击多大**｜补充 · 缓存 · 追问

10 个缓存节点按一致性哈希分片，总读流量 10 万 QPS，命中率 95%，数据库平时 5000 QPS、最多扛 1.5 万。一个缓存节点突然宕机，数据库会怎样？节点数该怎么定？

## A
**结论。** 宕机节点负责的那一份键全部变成 miss，数据库要多吃下「命中流量 ÷ 节点数」。10 个节点时多 9500 QPS，总共 14,500，几乎顶满上限。

**要点。**
- **算账：** 命中流量 9.5 万 ÷ 10 = 9500 QPS 变成 miss，数据库 5000 + 9500 = 14,500，余量只剩 500。
- **节点越多冲击越小：** 20 个节点多吃 4750，共 9750；只有 3 个节点则多吃约 31,667，共 36,667，是上限的 2.4 倍。
- **一致性哈希不等于没影响：** 它保证只重映射这一份键，但这份键在新节点上仍是冷的，要重新回填。
- **缓解办法：** 每个分片挂一个副本顶上；极热的键加本地缓存；回源请求合并；数据库前加限流。

**为什么。** 命中率把数据库「藏」在缓存后面，缓存每少一个节点就暴露一部分。暴露比例是 1/N，所以要按「数据库能吃下 1/N 的命中流量」反推节点数的下限。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个节点宕机后，数据库每秒读次数</text>
<text x="4" y="57" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">N=3</text>
<rect x="50" y="40" width="201.668" height="24" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="57" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">36,667</text>
<text x="4" y="97" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">N=10</text>
<rect x="50" y="80" width="79.75" height="24" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="97" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">14,500</text>
<text x="4" y="137" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">N=20</text>
<rect x="50" y="120" width="53.625" height="24" rx="3" stroke-width="1" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="137" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">9,750</text>
<line x1="132.5" y1="32" x2="132.5" y2="162" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="132.5" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据库上限 15,000</text>
</svg>

**面试里这样说。** 「10 个节点宕一个，冷掉 10% 的键，数据库多 9500 QPS，总共 1.45 万，已经贴着 1.5 万的上限。所以我按「数据库吃得下 1/N 命中流量」来定节点数，并给每个分片挂副本。」

**易错。**
- **只看平均命中率：** 95% 命中率下数据库看起来很闲，其实它的余量全靠缓存撑着。
- **用取模分片：** 节点增减时几乎所有键重映射，等于缓存整体清空。
