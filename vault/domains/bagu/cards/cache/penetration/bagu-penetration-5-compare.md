---
id: bagu-penetration-5-compare
node: a.cache.penetration
type: qa
step: 5
---
## Q
**缓存三大问题 · 区分与组合防线**｜追问

面试官：「线上一次故障里数据库被打满，你怎么判断是穿透、击穿还是雪崩？防线怎么组合，怎么监控？」

## A
**基本回答。** 看被打的数据来区分：查不存在的数据是穿透；单个热 key 过期是击穿；大批 key 失效或缓存整体不可用是雪崩。防线按层组合：入口校验、布隆过滤器加空值缓存挡穿透；互斥重建或逻辑过期挡击穿；TTL 抖动、多级缓存、限流降级挡雪崩。再用 `keyspace_hits / (keyspace_hits + keyspace_misses)` 监控命中率，命中率只掉 9 个点库压力就涨 10 倍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="90" y="6" width="160" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库被打满</text>
<line x1="170" y1="36" x2="170" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,52.0 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="52" width="220" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="71.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">被查的数据库里存在吗？</text>
<line x1="110" y1="82" x2="70" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,106.0 74.4,99.7 77.6,105.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="230" y1="82" x2="270" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,106.0 262.4,105.1 265.6,99.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="70" y="100" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不存在</text>
<text x="274" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存在</text>
<rect x="8" y="108" width="120" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">穿透</text>
<rect x="212" y="108" width="120" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围多大？</text>
<line x1="240" y1="138" x2="200" y2="158" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200.0,158.0 204.8,152.0 207.7,157.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="300" y1="138" x2="296" y2="158" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,158.0 294.2,150.5 300.5,151.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="158" width="90" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="195.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单个热 key</text>
<rect x="250" y="158" width="82" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="291.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大批/整体</text>
<line x1="195" y1="188" x2="195" y2="206" stroke-width="1.2" stroke="currentColor"/>
<polygon points="195.0,206.0 191.8,199.0 198.2,199.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="291" y1="188" x2="291" y2="206" stroke-width="1.2" stroke="currentColor"/>
<polygon points="291.0,206.0 287.8,199.0 294.2,199.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="206" width="90" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="195.0" y="225.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">击穿</text>
<rect x="250" y="206" width="82" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="291.0" y="225.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">雪崩</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓存永远</text>
<text x="8" y="175" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">建不起来</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">看命中率：按接口、key 前缀拆开看</text>
</svg>
从上往下问两个问题：被查的数据库里存在吗？不存在就是穿透；存在再问范围，单个热 key 是击穿，大批或整体是雪崩。
**容易错。**
- **只看整体命中率：** 平均值会掩盖局部问题，要按接口、key 前缀拆。
- **见到命中率低就加布隆：** 先判断类型，击穿和雪崩加布隆没用。
- **只治因不保库：** 数据库已经被打满时，应先限流降级。
- **把三种问题的防线混用：** 互斥重建救不了不存在的数据，布隆也救不了整体宕机。
**业务场景。** 大促开场读 QPS 10 万，命中率从 99% 掉到 90%，落库从 1000 涨到 1 万 QPS。先限流降级止血，再按 key 前缀拆命中率：某活动 ID 的查询未命中暴增，这些 ID 库里没有，判断是穿透，补布隆过滤器和空值缓存；若是热 key 整点失效就是击穿，若是大批 key 同刻失效或 Redis 不可用就是雪崩。
