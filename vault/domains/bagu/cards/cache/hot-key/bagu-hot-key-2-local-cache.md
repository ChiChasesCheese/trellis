---
id: bagu-hot-key-2-local-cache
node: a.cache.hot-key
type: qa
step: 2
---
## Q
**热 key · 本地缓存的 TTL 与一致性**｜必会

面试官：「你说给热 key 加本地缓存，TTL 设多少？数据变了，各台机器怎么办？」

## A
**基本回答。** 在应用进程内给热 key 加 1 到 5 秒的本地缓存，读请求被各个应用实例自己消化掉，不再全部打到 Redis。一致性的损失最多等于本地缓存的 TTL（存活时间），所以 TTL 就是你愿意容忍的旧数据时长。
**2026 亮点。** Redis / Valkey 的 client tracking：服务端记住每个连接读过的 key，被改、过期、淘汰时推送失效，连接断开则整体清空本地缓存，缓解各实例无法精确同步；代价是追踪表占内存，写频繁的 key 失效消息比命中收益还贵，部分官方客户端仍是实验性，TTL 仍保留兜底。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<rect x="8" y="12" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用实例1</text>
<text x="56.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地缓存 3 秒</text>
<line x1="56" y1="56" x2="56" y2="130" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="56.0,130.0 52.8,123.0 59.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="122" y="12" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用实例2</text>
<text x="170.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地缓存 3 秒</text>
<line x1="170" y1="56" x2="170" y2="130" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="170.0,130.0 166.8,123.0 173.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="236" y="12" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="30.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用实例3</text>
<text x="284.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地缓存 3 秒</text>
<line x1="284" y1="56" x2="284" y2="130" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="284.0,130.0 280.8,123.0 287.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="64" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回源很少</text>
<rect x="8" y="132" width="324" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 分片：只剩零星回源读</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">改了标题：各实例最多 3 秒后都读到新的</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TTL = 你愿意容忍的旧数据时长</text>
</svg>
每个应用实例先查自己进程里的本地缓存，3 秒才回一次 Redis；Redis 只会看到零星的回源读，改了标题，各实例最多 3 秒后都读到新的。
**容易错。**
- **以为本地缓存永远一致：** 一致性损失最多等于 TTL，是用一致性换吞吐。
- **所有实例同一时刻过期：** 同时回源又把 Redis 打了一遍；TTL 要加抖动，并用异步刷新或 singleflight（同 key 同时只放一个请求回源）合并。
- **不设容量上限：** 本地缓存无限涨会 OOM，要设最大条目数或权重并监控命中率；用软引用、弱引用代替上限也不行。
- **所有数据一视同仁：** 价格、库存这类关键字段不能放宽到几秒。
**举个例子。** 直播间标题缓存 TTL 3 秒、100 个实例：每实例每 3 秒最多回源 1 次，Redis 上这个 key 的读从 50 万次每秒降到约 33 次（100 ÷ 3）。标题改了，各实例最长再旧 3 秒；再配广播失效（Redis Pub/Sub 或 MQ，消息可能丢，TTL 兜底），大多数实例马上更新。价格、库存这类字段不能放宽，要绕过本地缓存或缩到亚秒。
