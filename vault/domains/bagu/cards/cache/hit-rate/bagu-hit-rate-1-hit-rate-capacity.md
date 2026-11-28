---
id: bagu-hit-rate-1-hit-rate-capacity
node: b.cache.hit-rate
type: qa
step: 1
---
## Q
**缓存命中率与容量估算**｜追问

面试官：「10 万读 QPS，缓存命中率从 99% 掉到 90%，数据库会怎样？缓存要预留多大容量？命中率突然下降怎么排查？」

## A
**基本回答。** 数据库 QPS = 读 QPS × (1 − 命中率)。命中率 99% 时数据库约 1000 QPS，掉到 90% 变成 1 万 QPS，是 10 倍。容量 = 条目数 × 单条大小 ÷ 0.7（留 30% 余量和碎片）：2000 万条 × 1KB = 20GB，约要规划 29GB 内存。命中率用 `keyspace_hits / (keyspace_hits + keyspace_misses)` 算（`INFO stats`），按 key 前缀拆开看能定位是哪类 key 出问题。突降时依次查：TTL 变短或大批 key 同时过期；key 变碎（把时间戳、随机数拼进了 key，比如某次发布后命中率 99% 掉到 90%）；内存到顶、`evicted_keys` 上涨；新业务带来大量冷数据；缓存刚重启或被清空。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读 10 万 QPS 时，落到数据库的 QPS</text>
<text x="10" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">命中 99%</text>
<rect x="86" y="26" width="24" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1000 QPS</text>
<text x="10" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">命中 95%</text>
<rect x="86" y="62" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5000 QPS</text>
<text x="10" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">命中 90%</text>
<rect x="86" y="98" width="240" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="206" y="115" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 万 QPS，是 10 倍</text>
<text x="10" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">命中率 = hits ÷ (hits + misses)</text>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">容量 = 条目数 × 单条大小 ÷ 0.7</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2000 万 × 1KB = 20GB，约规划 29GB</text>
<text x="10" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">核心读路径目标：95% 以上</text>
</svg>
三根横条是读 10 万 QPS 时落到数据库的请求数：命中率只掉 9 个百分点，数据库的负载就是 10 倍，所以高亮那一根要报警。
**容易错。**
- **只看总命中率：** 总量好看可能掩盖某个接口的暴跌，要按接口和 key 前缀分别统计。
- **容量不留余量：** 内存到顶会触发大量淘汰，命中率随之下降，要除以 0.7 留 30% 余量。
- **缓存所有数据：** 长尾数据几乎不会被重复读，缓存它只占内存，二八原则只缓存热的那 20%。
- **以为命中率掉 9 个点没事：** 没命中的比例从 1% 涨到 10%，数据库压力是 10 倍；核心读路径目标 95% 以上，低于就告警，不等数据库先扛不住。

